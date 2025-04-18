from fastapi import FastAPI
from bson.objectid import ObjectId
import pydantic
from database import client

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

app = FastAPI()

mydb = client["test"]
mycol = mydb['testdb']

@app.get('/')
async def HealthCheck():
    return {'status': 'ok'}
    
@app.get('/getmongo')
async def GetMongo():
    data = list(mycol.fing({}, {'_id': 0}).limit(10))
    print(data)
    return data

@app.get('/getuser')
async def GetUser(id=None):
    if id is None:
        return "id를 입력하세요."
    result = list(mycol.find({'_id': id}, {'_id': 0}))
    if result:
        print(result)
        return result
    else:
        return "id를 찾을 수 없습니다."

@app.get('/useradd')
async def UesrAdd(id=None, name=None):
    if (id is None) or (name is None):
        return "id, name를 입력하세요."
    else:
        uesr = dict(id=id, name=name)
        mycol.insert_one(uesr)
        result = mycol.find({'id': id}, {'_id': 0})
        print(result)
        return result

@app.get('/userupdate')
async def UesrUpdate(id=None, name=None):
    if (id is None) or (name is None):
        return "id, name를 입력하세요."
    else:
        uesr = mycol.find({'id': id}, {'_id': 0})
        if uesr:
            user['name'] = name
            mycol.update_one({'id': id}, {'$set': user})
            result = mycol.find({'id': id}, {'_id': 0})
            print(result)
            return result
        else:
            return "id를 찾을 수 없습니다."

@app.get('/userdelete')
async def UesrDelete(id=None):
    if (id is None):
        return "id를 입력하세요."
    else:
        uesr = mycol.find({'id': id}, {'_id': 0})
        if uesr:
            mycol.delete_one({'id': id})
            result = list(mycol.find({}, {'_id': 0}))
            print(result)
            return result
        else:
            return "id를 찾을 수 없습니다."