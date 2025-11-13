from fastapi import APIRouter
from pydantic import BaseModel
from app.rag import vector_db
from app.graph import model
from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger


router = APIRouter()

class Query(BaseModel):
    query: str

@router.post("/query")
async def index(text:Query):

    results = await vector_db.query(text.query)

    logger.info(results["documents"])



    answer = model.invoke([

        SystemMessage(content = 'you are world class answer provider with the context given and dont answer outside the context'),
        HumanMessage(content = f"Here is the context {results["documents"]}"),
        HumanMessage(content = f"Here is the query {text.query}")

    ])

    return {"results": answer.content}
