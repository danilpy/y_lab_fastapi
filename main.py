import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title='YLab_University'
)

BASE_API_URL = '/api/v1/'

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
