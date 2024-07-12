import asyncio
from langchain_core.language_models.llms import LLM
from typing import Any, Dict, Iterator, List, Mapping, Optional
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from .chatgpt import ChatGPT

class BrowserGPT(LLM):
    chatbot_url="https://chatgpt.com/"
    chatbot = ChatGPT(chatbot_url=chatbot_url)
    initialized = False

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        #self._initialize().__await__()
        return  self.chatbot.query(prompt)
    
    async def _acall(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        #await self._ainitialize()
        return await self.chatbot.aquery(prompt)

    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model. Used for logging purposes only."""
        return "browser_gpt"


def main():
    llm = BrowserGPT()
    answer = llm.invoke("How are you ?")
    print(answer)
    
    answer = llm.invoke("Do you know Benin ?")
    print(answer)
    
    

if __name__ == '__main__':
    main()