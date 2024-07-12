from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from operator import itemgetter


class NL2SQLChain():
    def __init__(self, db, llm, extract_query, extract_answer, rephrase_prompt, query_prompt=None, verbose=True) -> None:
        self.db = db
        self.llm = llm
        self.query_prompt = query_prompt
        self.rephrase_prompt = rephrase_prompt
        self.extract_query = extract_query
        self.extract_answer = extract_answer
        self.verbose = verbose

        self.setup()

    def setup(self):
        # Create SQL query generator
        query_generator = create_sql_query_chain(
            self.llm, self.db, prompt=self.query_prompt)

        # Create SQL query executor
        query_executor = QuerySQLDataBaseTool(
            db=self.db, verbose=self.verbose)

        # Creaate rephrase_answer runnable
        rephrase_answer = self.rephrase_prompt | self.llm | StrOutputParser()

        # Chain to generate and execute SQL query, and rephrase answer
        self.chain = (
            RunnablePassthrough
            .assign(query=query_generator | RunnableLambda(self.extract_query))
            .assign(result=itemgetter("query") | query_executor)
            .assign(answer=rephrase_answer | RunnableLambda(self.extract_answer))
        )

        # Chain to generate SQL query
        self.query_chain = (
            RunnablePassthrough
            .assign(query=query_generator | RunnableLambda(self.extract_query))
        )

    def invoke(self, req):
        return self.chain.invoke(req)

    async def ainvoke(self, req):
        return await self.chain.ainvoke(req)

    def query(self, req):
        return self.query_chain.invoke(req)

    async def aquery(self, req):
        return await self.query_chain.ainvoke(req)

    def test(self, req):
        return self.llm.invoke(req["question"])
