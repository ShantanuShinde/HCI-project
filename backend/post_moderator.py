from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3


class PostModerator:
    def __init__(self, model_name: str = "llama2", base_url: str = "http://localhost:11434"):
        self._config = {"configurable": {"thread_id": "1"}}
        self._system_prompt = (
            "You are a content moderator bot. Your task is to evaluate the text that is passed to you for appropriateness, offensiveness and discrimination."
            "You need to flag the text only if it contains hate speech against any group and minorities, including but not limited to: LGBTQ+, racial minorities, disabled people, religious minorities, etc."
            "You should also flag text with inappropriate content, including but not limited to: explicit sexual content, extreme violence, self-harm, etc."
            "You should NOT flag text that doesn't contain any of the above, and if the text is not targeting any group or individual with the above but mentioning those things in a neutral or discussion context."
            "If the text is flagged, you should respond with 'YES', otherwise respond with 'NO'."
            "DO NOT give any other responses, only 'YES' or 'NO'. Not explanation for the response."
        )

        self.model = ChatOllama(model=model_name, temperature=0, base_url=base_url)
        # conn_string = "dbname=mydb user=postgres password=postgres host=localhost port=5432"
        # with PostgresSaver.from_conn_string(conn_string) as postgres_saver:
        #     postgres_saver.setup()
        # self.react_agent = create_react_agent(model=self.model, tools=[], prompt=self.system_prompt, checkpointer=postgres_saver)
        conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
        sqlite_saver = SqliteSaver(conn)
        self.react_agent = create_react_agent(model=self.model, tools=[], prompt=self.system_prompt, checkpointer=sqlite_saver)

    @property
    def system_prompt(self) -> str:
        return self._system_prompt

    def moderate(self, text: str) -> bool:
        prompt = f"Text: {text}"
        for event in self.react_agent.stream({"messages": [{"role": "user", "content": prompt}]}, config=self._config, stream_mode="values"):
            if len(event["messages"][-1].response_metadata) != 0:
                return event["messages"][-1].content == "YES"
        return False
    
if __name__ == "__main__":
    moderator = PostModerator()
    test_texts = [
        "I love everyone equally.",
        "I hate all people of [a certain race].",
        "This is a normal post about daily life."]
    for text in test_texts:
        print(f"Text: {text} -> Inappropriate: {moderator.moderate(text)}")