import google.generativeai as genai
import os
from langchain_core.language_models.llms import LLM
from typing import Any, List, Optional
from langchain_core.callbacks.manager import CallbackManagerForLLMRun

from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


class GoogleLLM(LLM):
    model_id = "models/text-bison-001"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        response = genai.generate_text(
            prompt=prompt, model=self.model_id, stop_sequences=stop)
        return response.result

    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model. Used for logging purposes only."""
        return "google"


def main():
    llm = GoogleLLM()
    answer = llm.invoke("How are you ?")
    print(answer)

    answer = llm.invoke("Do you know Benin ?")
    print(answer)


if __name__ == '__main__':
    main()
