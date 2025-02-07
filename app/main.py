import json
import logging
from typing import Any, Dict, List
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile,status,Response
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from config.settings import Settings
from sqlalchemy.orm import Session
from data import crud, media
from data import schemas
from data import dependencies
from data import models
from apis import services
import sys
import os 

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


app = FastAPI()
 
settings = Settings()

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ALLOWED_ORIGINS], 
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=[settings.ALLOW_METHODS],  
    allow_headers=[settings.ALLOW_HEADERS],  
)


@app.get("/live")
def root():
    return {"status": "Running...", "service_name": "jbm_Application"}


@app.get("/users/")
def get_users(db: Session = Depends(dependencies.get_db)):
    get_all_user=services.get_user(db=db)
    return get_all_user

@app.get("/users/{adhaar_ID}")
async def queries(response: Response,ID:str, 
                    db: Session = Depends(dependencies.get_db) ):
    """
    Return queries that are saved in DB. 

    """  
    return services.get_by_adhar_id(db=db,adhar_id=ID)

@app.get("/users/{pincode}")
async def queries(response: Response,pincode:str, 
                    db: Session = Depends(dependencies.get_db)):
    """
    Return queries that are saved in DB. 

    """  
    return services.get_by_pincode(db=db,pincode=pincode)
    
@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    """API to receive an image and store it in S3."""
    s3_key = media.generate_s3_key(file.filename)

    try:
        image_url = media.upload_to_s3(file.file, s3_key)
        return {"message": "Image uploaded successfully", "image_url": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/users/", response_model=Dict[str, Any])
async def create_user(
    queries_to_add: List[schemas.UserProfileCreate],  
    response: Response,  
    db: Session = Depends(dependencies.get_db)
):
    created_users = [] 
    for user_data in queries_to_add:
        log.info(user_data)

        # Add user to DB
        user_id = services.add_user(db=db, user_to_add=user_data)

        created_users.append({
            "user_id": str(user_id),
            "status": "created"
        })

    return {"status": "200", "created_users": created_users}

@app.put("/users/", response_model=Dict[str, Any])
async def update_users(
    queries_to_update: List[schemas.UserProfileCreate],  
    response: Response,  
    db: Session = Depends(dependencies.get_db)
):
    updated_users = []  
    
    for user_data in queries_to_update:
        log.info(f"Updating user data: {user_data}")
        user_id = services.updated_user(db=db, user_to_update=user_data)
        updated_users.append({
            "user_id": user_id,
            "status": "updated"
        })
    
    return {"status":"200","updated_users": updated_users}


@app.delete("/users/{user_id}", response_model=Dict[str, str])
async def delete_user(
    user_id: str,  
    db: Session = Depends(dependencies.get_db)
):
    try:
        deleted = services.delete_user(db=db, user_id=user_id)  

    except:
        raise HTTPException(status_code=404, detail="User not found") 
    
    return {"status":"200","message": f"User {user_id} deleted successfully"}  

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(dependencies.get_db)):

    # Read the file content
    file_content = await file.read()
    log.debug(file_content)
    print(file_content)
    processed_data = services.process_csv_data(file_content,db=db)
    return {"message": "CSV data has been successfully uploaded and saved to the database."}


@app.get("/unit/")
def get_users(db: Session = Depends(dependencies.get_db)):
    get_all_unit=services.get_unit(db=db)
    return get_all_unit

@app.post("/unit/", response_model=Dict[str, Any])
async def create_unit(
    unit_to_add: List[schemas.UnitCreate],  
    response: Response,  
    db: Session = Depends(dependencies.get_db)
):
    created_units = []  # List to store created user details
    
    for unit_data in unit_to_add:
        log.info(unit_data)

        # Add user to DB
        unit_id = services.add_unit(db=db, unit_to_add=unit_data)

        created_units.append({
            "user_id": unit_id.unitCode,
            "status_code": "200",
            "status": "thithili_unit_created_successfully"
            })

    return { "unit": created_units}

@app.delete("/unit/{unit_code}", response_model=Dict[str, str])
async def delete_by_unitID(
    unit_code: str,  
    db: Session = Depends(dependencies.get_db)
):
    try:
        deleted = services.delete_unit(db=db, unit_code=unit_code)  

    except:
        raise HTTPException(status_code=404, detail="User not found") 
    
    return {"status":"200","message": f"User {unit_code} deleted successfully"}  


    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8084)