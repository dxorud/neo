from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def HealthCheck():
    return {"ststus": "ok"}

@app.get('/hello')
async def Hello():
    return {"message" : "Hello World"}

@app.get('/random')
async def Random(max=None):
    import random
    
    if max in None:
        max = 10
    else:
        max = int(max)
    return {"return number": random.randint(1, max)}