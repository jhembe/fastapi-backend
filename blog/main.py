from fastapi import FastAPI,Depends,status,Response,HTTPException
from . import schemas,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session 
from typing import List     

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog/', status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog,db: Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)    
    db.commit()
    db.refresh(new_blog)
    return new_blog

# Getting the blog from the database
@app.get('/blog',status_code=200, response_model=List[schemas.ShowBlog])
def all_blogs(db: Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

#getting a particular id by passing it's reference throught the endpoint
@app.get('/blog/{id}',status_code=200,response_model=schemas.ShowBlog)
def show_one(id,response:Response,db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'The blog with id {id} does not exist')
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f'The blog with id {id} does not exist'}
    return blog

#deleting a content of a blog
@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id,db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The blog with ID {id} does not exist")
    blog.delete(synchronize_session = False)
    db.commit()
    return 'done'

#updating blog contents 
@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request:schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The Blog with ID {id} doesn't exist")
    blog.update(request.dict())
    db.commit()
    return {'detail':f'A Blog with ID : {id}, was updated succesfully'}

#deleting all
@app.delete('/blog/',status_code=status.HTTP_204_NO_CONTENT)
def delete_all(db: Session=Depends(get_db)):
    blogs = db.query(models.Blog).all().delete(synchronize_session = False)
    db.commit()
    return 'done'


## for the user
@app.post('/user/')
def create_user(request: schemas.User,db:Session = Depends(get_db)):
    new_user = models.User(name=request.name,email=request.email,password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return request