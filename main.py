from fastapi import FastAPI
import uvicorn
from app import endpoints
from settings import settings



app = FastAPI()


app.include_router(endpoints.router)



if __name__ == "__main__":
    uvicorn.run(app)
