import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from docs.conf import docs_tags_metadata

from database.sql_db import bigquery
from database.model import RequestBody, ChatResponseBody, QueryResponseBody

from llm.llm_model import LLMModel
from llm.output_processing import get_extractors
from llm.prompt import get_prompts
from llm.few_shot_examples import get_few_shot_examples_prompt
from chain.nl2sql_chain import NL2SQLChain

logging.basicConfig(level=logging.INFO)
load_dotenv()
origins = [
    "http://localhost:3000",
]

include_tables = [
    "t_total_login",
    "t_failed_login",
    "t_reset_passeword",
    # "lite_manage_tf",
    # "tf_signup_authtype"
]

# Construct db for db operations (can be mysql or postgres)
db = bigquery(
    project="ciam-gcs-dsip",
    dataset="DataChat",
    service_account_key_path="./.keys/ciam-gcs-dsip.data-read.json",
    # include_tables=include_tables,
)


model_type = os.environ.get("MODEL_TYPE")
embedding_type = os.environ.get("EMBEDDING_TYPE")
use_axamples = os.environ.get("USE_EXAMPLES")

model = LLMModel(model_type)
llm = model.get_llm()
query_prompt, rephrase_prompt = get_prompts(model_type)
extract_answer, extract_query = get_extractors(model_type)

if use_axamples == "yes":
    query_prompt = get_few_shot_examples_prompt(embedding_type)
    logging.info("Using few shot examples")

# Print example of prompt the model sends to the LLM
logging.info(query_prompt.format(input="Nombre de logins pour lmes", top_k=5,
             table_info=db.table_info, dialect="GoogleSQL"))

nl2sql = NL2SQLChain(
    db=db,
    llm=llm,
    extract_query=extract_query,
    extract_answer=extract_answer,
    query_prompt=query_prompt,
    rephrase_prompt=rephrase_prompt
)

app = FastAPI(
    title="Text2SQLChabot",
    openapi_tags=docs_tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["hello"])
def hello():
    return {"Hello": "Text2SQL"}


@app.post("/query", tags=["chat"])
async def query(req: RequestBody) -> QueryResponseBody:
    return await nl2sql.aquery({"question": req.message})


@app.post("/chat", tags=["chat"])
async def chatbot(req: RequestBody) -> ChatResponseBody:
    return await nl2sql.ainvoke({"question": req.message})
