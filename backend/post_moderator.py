from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from sentence_transformers import SentenceTransformer, util


class PostModerator:
    """
     A content moderator that uses a language model to evaluate text for appropriateness.
     The moderator can be updated with new patterns of inappropriate text to improve its accuracy.
     Requires an Ollama server running locally with the specified model (default: "llama3:8b") at the specified base URL.
    """
    def __init__(self, model_name: str = "llama3:8b", base_url: str = "http://localhost:11434"):
        """
        Initialize the PostModerator with a language model.
        Args:
            model_name (str): The name of the language model to use (default: "llama3:8b").
            base_url (str): The base URL of the Ollama server (default: "http://localhost:11434").
        """
        self._config = {"configurable": {"thread_id": "1"}}
        self._base_system_prompt = (
            "You are a content moderator bot. Your task is to evaluate the text that is passed to you for appropriateness, offensiveness and discrimination.\n"
            "You need to flag the text only if it contains hate speech against any group and minorities, including but not limited to: LGBTQ+, racial minorities, disabled people, religious minorities, etc.\n"
            "You should also flag text with inappropriate content, including but not limited to: explicit sexual content, extreme violence, self-harm, etc.\n"
            "DO NOT give any responses other than 'YES' or 'NO'. Not explanation for the response.\n"
        )
        self._system_prompt = self._base_system_prompt

        self.to_flag = set()
        self.not_flag = set()

        self._sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')

        self.model = ChatOllama(model=model_name, temperature=0, base_url=base_url)

        conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
        self.sqlite_saver = SqliteSaver(conn)

        self.react_agent = create_react_agent(model=self.model, tools=[], prompt=self.system_prompt, checkpointer=self.sqlite_saver)
        self.react_agent_unfiltered = create_react_agent(model=self.model, tools=[], prompt=self._base_system_prompt) 

    @property
    def system_prompt(self) -> str:
        return self._system_prompt

    def _get_sentece_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate the cosine similarity between two texts using sentence embeddings.
        Args:
            text1 (str): The first text.
            text2 (str): The second text.
        Returns:
            Cosine similarity score between the two texts.
        """
        embeddings1 = self._sentence_transformer.encode(text1, convert_to_tensor=True)
        embeddings2 = self._sentence_transformer.encode(text2, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(embeddings1, embeddings2)
        return similarity.item()
    
    def _find_similar_texts(self, new_pattern: str, patterns: set, threshold: float = 0.6) -> bool:
        """
        Find similar texts in the given set of patterns.
        Args:
            new_pattern (str): The new pattern to compare against existing patterns.
            patterns (set): A set of existing patterns to compare with.
            threshold (float): The similarity threshold (default: 0.6).
        Returns:
            List of patterns that are similar to the new pattern.
        """

        return [pattern for pattern in patterns if self._get_sentece_similarity(new_pattern, pattern) >= threshold]
    
    def _construct_system_prompt(self) -> str:
        prompt = self._base_system_prompt
        prompt += "\nAlso if user provides you with examples of inappropriate or appropriate text, update your moderation criteria accordingly."
        if len(self.to_flag) > 0:
            texts_to_flag = "\n".join(self.to_flag)
            prompt += f"\nFrom now on, also flag as inappropriate any text similar to: \n{texts_to_flag}"
        if len(self.not_flag) > 0:
            texts_to_not_flag = "\n".join(self.not_flag)
            prompt += f"\nFrom now on, do NOT flag as inappropriate any text similar to: \n{texts_to_not_flag}"
        return prompt

    def moderate(self, text: str, filtered: bool = True) -> bool:
        """
        Evaluate the given text for appropriateness.
        Args:
            text (str): The text to evaluate.
            filtered (bool): Whether to use the filtered agent with updated patterns.
        Returns:
            True if the text is inappropriate, False otherwise.
        """
        prompt = f"Text: {text}"
        agent = self.react_agent if filtered else self.react_agent_unfiltered
        for event in agent.stream({"messages": [{"role": "user", "content": prompt}]}, config=self._config, stream_mode="values"):
            if len(event["messages"][-1].response_metadata) != 0:
                return event["messages"][-1].content == "YES"
        return False

    def add_inappropriate_pattern(self, pattern: str):
        """
        Add a new pattern or example of inappropriate text. The moderator will flag similar text as inappropriate from now on.
        Args:
            pattern (str): A new example or pattern of inappropriate text.
        """
        self.to_flag.add(pattern)
        similar_texts = self._find_similar_texts(pattern, self.not_flag)
        self.not_flag.difference_update(similar_texts)

        self._system_prompt = self._construct_system_prompt()
        self.react_agent = create_react_agent(model=self.model, tools=[], prompt=self._system_prompt, checkpointer=self.sqlite_saver)

    def add_appropriate_pattern(self, pattern: str):
        """
        Add a new pattern or example of appropriate text. The moderator will NOT flag similar text as inappropriate from now on.
        Args:
            pattern (str): A new example or pattern of appropriate text.
        """
        self.not_flag.add(pattern)
        similar_texts = self._find_similar_texts(pattern, self.to_flag)
        self.to_flag.difference_update(similar_texts)

        self._system_prompt = self._construct_system_prompt()
        self.react_agent = create_react_agent(model=self.model, tools=[], prompt=self._system_prompt, checkpointer=self.sqlite_saver)

if __name__ == "__main__":
    moderator = PostModerator()
    test_texts = [
        "I love everyone equally.",
        "I hate all people of [a certain race].",
        "This is a normal post about daily life."]
    for text in test_texts:
        print(f"Text: {text} -> Inappropriate: {moderator.moderate(text)}")