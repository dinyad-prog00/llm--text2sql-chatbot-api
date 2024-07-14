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

few_shot_system_prompt= """
You are a {dialect} expert. Given an input question, first create a syntactically correct {dialect} query to run.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per {dialect}. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Here is the relevant table info: 
{table_info}
Below are a number of examples of questions and their corresponding SQL queries.
"""


def get_prompts(model_type):
    if model_type == "pipable":
        return pipable_query_prompt, rephrase_prompt
    else:
        return None, rephrase_prompt
