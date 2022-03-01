from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn
from . import schemas,models
from .database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
@app.get('/blog')
def index(limit,published:bool):
    # only get 10 published blogs
    if published:
        return {'data':f'{limit} published blogs from the database'} 
    else:
        return {'data':f'{limit} blogs from the database'}
# for the second routing, i need to keep some dynamic routing

@app.get('/blog/unpublished')
def unpublished():
    return {'data':'All unpublished blogs'}

@app.get('/blog/{id}')
def show(id:int):
    return {'data':id}

@app.get('/blog/{id}/comments')
def comments(id):
    #fetch comment's of id=id
    return {'data':{'1','2'}}
    
class Blog(BaseModel):
    title:str
    body:str 
    published:Optional[bool]

@app.post('/blog')
def create_blog(blog:Blog):
    return {'data':f"Blog is created with {blog.title} and it's body says {blog.body}. It's published status is {blog.published}."}




# if __name__ == "__main__":
#     uvicorn.run(app,host="localhost",port=9000)