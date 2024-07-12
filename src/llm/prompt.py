from langchain_core.prompts import PromptTemplate

pipable_query_prompt = PromptTemplate.from_template(
    """
        {top_k}
        <schema>{table_info}</schema>
        <question>{input}</question>
        <sql>
    """
)

rephrase_prompt = PromptTemplate.from_template(
    """
    Given the following user question, corresponding SQL query, and SQL result, provide a complete sentence in response with verbs.
    Question: {question}
    SQL Query: {query}
    SQL Result: {result}
    Answer:
    """
)


def get_prompts(model_type):
    if model_type == "pipable":
        return pipable_query_prompt, rephrase_prompt
    else:
        return None, rephrase_prompt
