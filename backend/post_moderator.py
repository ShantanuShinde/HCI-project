from langchain_community.chat_models import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver


class PostModerator:
    def __init__(self, model_name: str = "llama2", base_url: str = "http://localhost:11434"):
        self.model = ChatOllama(model_name=model_name, base_url=base_url)
        self.memory_saver = InMemorySaver()
        self.react_agent = create_react_agent(model=self.model, tools=[], prompt=self.system_prompt, checkpointer=self.memory_saver)

        self._config = {"configurable": {"thread_id": "1"}}
        self._system_prompt = (
            "You are a content moderator bot. Your task is to evaluate the text that is passed to you for appropriateness, offensiveness and discrimination."
            "You need to flag the text only if it contains hate speech against any group and minorities, including but not limited to: LGBTQ+, racial minorities, disabled people, religious minorities, etc."
            "You should also flag text with inappropriate content, including but not limited to: explicit sexual content, extreme violence, self-harm, etc."
            "You should NOT flag text that doesn't contain any of the above, and if the text is not targeting any group or individual with the above but mentioning those things in a neutral or discussion context."
            "If the text is flagged, you should respond with 'NO', otherwise respond with 'YES'."
            "DO NOT give any other responses, only 'YES' or 'NO'. Not explanation for the response."
        )

    @property
    def system_prompt(self) -> str:
        return self._system_prompt

    def moderate(self, text: str) -> bool:
        prompt = f"Text: {text}"
        for event in self.react_agent.stream({"messages": [{"role": "user", "content": prompt}]}, config=self._config, stream_mode="values"):
            if len(event["messages"][-1].response_metadata) != 0:
                return event["messages"][-1].content == "YES"
        return False