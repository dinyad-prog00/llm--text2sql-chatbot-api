from pydantic import BaseModel

class RequestBody(BaseModel):
    message: str
    
class ChatResponseBody(BaseModel):
    question: str 
    query: str 
    result: str
    answer: str

class QueryResponseBody(BaseModel):
    question: str 
    query: str  
     
    
