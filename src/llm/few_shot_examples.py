from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, FewShotChatMessagePromptTemplate, PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from llm.prompt import few_shot_system_prompt
from llm.utils import read_examples_data
from llm.embeddings import get_embeddings


def get_few_shot_examples_prompt(emdedding_type="hf"):
    embeddings = get_embeddings(emdedding_type)
    examples = read_examples_data()
    vectorstore = Chroma()
    vectorstore.delete_collection()
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        embeddings,
        vectorstore,
        k=2,
        input_keys=["input"],
    )

    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{query}"),
        ]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        example_selector=example_selector,
        input_variables=["input", "top_k"],
    )

    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", few_shot_system_prompt),
            few_shot_prompt,
            ("human", "{input}"),
        ]
    )

    return final_prompt


if __name__ == "__main__":
    prompt = get_few_shot_examples_prompt(emdedding_type="hf")
    print(prompt.format(input="How many products are there?",
          top_k=5, table_info="table infos", dialect="GoogleSQL"))
