# firstly import fastapi
from fastapi import FastAPI, HTTPException, status
# importing routes from routers file
from .routers import products, categories
from .models import ProductModel, CategoryModel
from .data.db import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os


# initiate the database and create the tables 
ProductModel.Base.metadata.create_all(bind=engine)
CategoryModel.Base.metadata.create_all(bind=engine) 

# create an instance of fastapi and call it
app = FastAPI()

app.mount("/images", StaticFiles(directory="api/images"), name="images") 

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes/path operations
@app.get('/') # decorator initialized by '@' then the instance of fastapi then the http method then the path or route'/'
def home():  # function
    return {'message': 'this is the home/login path use /docs for more infos'}



## get the image src for the frontend
@app.get("/image/{filename}")
async def read_image(filename: str):
    files = os.listdir("api/images")
    if filename in files:
        return FileResponse(f"api/images/{filename}", media_type="image/jpeg")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image does not exist")


#products route
app.include_router(products.router)
app.include_router(categories.router)
