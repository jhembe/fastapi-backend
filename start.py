from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'data':{'name':'Joseph',"age":19,"Father":"Gabriel","Mother":"Canisius"}}

@app.get('/about')
def about():
    return {'data':{'Joseph':"He's one of a kind"}}