import asyncio
from langchain_core.language_models.llms import LLM
from typing import Any, Dict, Iterator, List, Mapping, Optional
from langchain_core.callbacks.manager import CallbackManagerForLLMRun

import requests


class LMStudioLLM(LLM):
    endpoint: str = None

    def _call(self,
              prompt: str,
              stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              **kwargs: Any,) -> str:
        print(kwargs)
        response = requests.post(
            self.endpoint,
            json={
                "model": "chatdb/natural-sql-7b-GGUF",
                "prompt": prompt,
                "temperature": 0.7,
                "max_tokens": 25,
                "stream": False
            }
        )
        response.raise_for_status()  # Ensure we catch any HTTP errors
        response_json = response.json()
        return response_json['choices'][0]["text"]

    @property
    def _identifying_params(self) -> dict:
        return {'endpoint': self.endpoint}

    @property
    def _llm_type(self) -> str:
        return "lmstudio_llm"


def main():
    llm = LMStudioLLM(endpoint="http://localhost:1234/v1/completions")
    
    answer = llm.invoke("select hello")
    print(answer)

    answer = llm.invoke("Do you know Benin ?")
    print(answer)

    answer = llm.invoke("What is Benin ?")
    print(answer)


if __name__ == '__main__':
    main()
