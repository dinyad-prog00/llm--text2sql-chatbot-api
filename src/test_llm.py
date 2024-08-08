from llm.llm_model import LLMModel

model_type = "google"
model = LLMModel(model_type)
llm = model.get_llm()
answer = llm.invoke("How are you?")
print(answer)
