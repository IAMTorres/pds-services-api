from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from api.router import api_router

app = FastAPI()
app.include_router(api_router)

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
