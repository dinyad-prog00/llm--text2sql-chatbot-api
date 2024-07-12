from langchain_huggingface import HuggingFacePipeline
from langchain_openai import ChatOpenAI
from llm.lmstudio_local_server import LMStudioLLM
from .config import get_device_map
from llm.google import GoogleLLM
# from .browser_gpt import BrowserGPT

class LLMModel():
    def __init__(self, model_type, model_id=None):
        self.model_type = model_type
        self.model_id = model_id
        if model_type == "chatdb":
            self.llm = self.chatdb()
        if model_type == "google":
            self.llm = self.google()
        if model_id == "openai":
            self.llm = self.openai()
        if model_type == "pipable":
            self.llm = self.pipable()
        if model_type == "lmstudio":
            self.llm = self.lmstudio()

    def get_llm(self):
        return self.llm

    def chatdb(self, model_id="chatdb/natural-sql-7b"):
        return self.__hf_build(model_id, get_device_map(8))

    def pipable(self, model_id="PipableAI/pip-sql-1.3b"):
        return self.__hf_build(model_id, get_device_map(15))

    def google(self, model_id="models/text-bison-001"):
        return GoogleLLM(model_id=model_id)

    def openai(self, model_id="gpt-3.5-turbo"):
        return ChatOpenAI(model=model_id)

    def lmstudio(self):
        return LMStudioLLM(endpoint="http://localhost:1234/v1/completions")

    # def gpt(self):
    #     return BrowserGPT()

    def __hf_build(sefl,  model_id, device_map, task="text-generation"):
        return HuggingFacePipeline.from_model_id(
            model_id=model_id,
            task=task,
            device=None,
            # device_map=device_map,
            pipeline_kwargs={
                "max_new_tokens": 100,
                # "top_k": 50,
                # "temperature": 0.1,
                'num_return_sequences': 1,
                'eos_token_id': 100001,
                'pad_token_id': 100001,
                'do_sample': False,
                'num_beams': 1,
                # 'skip_special_tokens': True
            },
            model_kwargs={
                'device_map': device_map,
                'offload_folder': "/tmp/.offload",
                'load_in_4bit': True,
                'llm_int8_enable_fp32_cpu_offload': True
            }
        )
