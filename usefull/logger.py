from fastapi import FastAPI
import uvicorn
import logging

app = FastAPI()



@app.get("/")
def get():
    return 1

@app.get("/1")
def geterror(str: str):
    int(str)/0


# if __name__ == "__main__":
#     uvicorn.run("logger:app", reload=True, log_config=LOGGING_CONFIG)