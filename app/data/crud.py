
from datetime import datetime
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import schemas, models
from data.models import State_details
from config.settings import Settings
import logging

#
# IMPORTANT: Change these queries to consider tenant ID and current user in the context.
#
settings = Settings()

# initialize logger
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)


def add_user(db: Session,userToAdd: schemas.UserProfileCreate):
    log.debug("entering crud")
    added_user = models.User( fullName = userToAdd.fullName,
                                 aadhaarNumber = userToAdd.aadhaarNumber, 
                                 fatherAdhaar=userToAdd.fatherAdhaar,
                                 motherAadhaar=userToAdd.motherAadhaar,
                                 gender=userToAdd.gender,
                                 dateOfBirth=userToAdd.dateOfBirth,
                                 mobileNumber=userToAdd.mobileNumber,
                                 fatherName=userToAdd.fatherName,
                                 fatherMobile=userToAdd.fatherMobile,
                                 motherMobile=userToAdd.mobileNumber,
                                 motherName=userToAdd.motherName,
                                 dateOfJoin=userToAdd.dateOfJoin,
                                 address=userToAdd.address,
                                 area=userToAdd.area,
                                 pinCode=userToAdd.pinCode,
                                 profileAvatar=userToAdd.profileAvatar,
                                 latitude=userToAdd.latitude,
                                 longitude=userToAdd.longitude,
                                 createdBy = userToAdd.createdBy,
                                 createdOn = userToAdd.createdOn
                                 
                                 )
    db.add(added_user)
    db.commit()
    db.refresh(added_user)
    return added_user.aadhaarNumber


def update_user(db: Session, userToAdd: schemas.UserProfileCreate):
    """
    Adds a new user record. If a user with the same aadhaarNumber exists, 
    a new row is created instead of updating the existing row.
    """
    # Fetch latest version of the user based on AadhaarNumber
    existing_user = db.query(models.User).filter(
        models.User.aadhaarNumber == userToAdd.aadhaarNumber
    ).order_by(models.User.user_id.desc()).first()  # Get latest entry if exists
    
    if existing_user:
        log.info(f"User with Aadhaar {userToAdd.aadhaarNumber} exists, creating a new version.")

    # Create a new user entry (even if user exists, we create a new row)
    new_user = models.User(
        fullName=userToAdd.fullName or (existing_user.fullName if existing_user else None),
        aadhaarNumber=userToAdd.aadhaarNumber,  # Keep same Aadhaar ID
        fatherAdhaar=userToAdd.fatherAdhaar or (existing_user.gender if existing_user else None),
        motherAadhaar=userToAdd.motherAadhaar or (existing_user.motherAadhaar if existing_user else None),
        gender=userToAdd.gender or (existing_user.gender if existing_user else None),
        dateOfBirth=userToAdd.dateOfBirth or (existing_user.dateOfBirth if existing_user else None),
        fatherMobile=userToAdd.fatherMobile or (existing_user.fatherMobile if existing_user else None),
        motherMobile=userToAdd.fatherMobile or (existing_user.motherMobile if existing_user else None),
        mobileNumber=userToAdd.mobileNumber or (existing_user.mobileNumber if existing_user else None),
        fatherName=userToAdd.fatherName or (existing_user.fatherName if existing_user else None),
        motherName=userToAdd.motherName or (existing_user.motherName if existing_user else None),
        dateOfJoin=userToAdd.dateOfJoin or (existing_user.dateOfJoin if existing_user else None),
        address=userToAdd.address or (existing_user.address if existing_user else None),
        area=userToAdd.area or (existing_user.area if existing_user else None),
        pinCode=userToAdd.pinCode or (existing_user.pinCode if existing_user else None),
        profileAvatar=userToAdd.profileAvatar or (existing_user.profileAvatar if existing_user else None),
        latitude=userToAdd.latitude or (existing_user.latitude if existing_user else None),
        longitude=userToAdd.longitude or (existing_user.longitude if existing_user else None),
        createdBy=existing_user.createdBy if existing_user else userToAdd.createdBy,  # Preserve original creato
        createdOn=existing_user.createdOn ,
        updatedBy=userToAdd.aadhaarNumber,  # Store the user who updated
        updatedOn=str(datetime.utcnow().timestamp())  # Store current timestamp as update time
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user.aadhaarNumber  # Return AadhaarNumber as confirmation
def deleted_user(db: Session, adhar_id: str):
    user=db.query(models.User).filter(models.User.aadhaarNumber == adhar_id).first()
    db.delete(user)  # Delete the user
    db.commit()
    
def deleted_units(db: Session, units: str):
    user=db.query(models.thithili_unit).filter(models.thithili_unit.unitCode== units).first()
    db.delete(user)  # Delete the user
    db.commit()

def get_by_adhar_id(db: Session, adhar_id: str):
    return db.query(models.User).filter(models.User.aadhaarNumber == adhar_id).order_by(models.User.updatedOn.desc()) .first()

def get_by_pincode(db: Session, pincode: str):
    return db.query(models.User).filter(models.User.pinCode == pincode).all()
def get_user(db: Session):
    return db.query(models.User).all()
def get_unit_all(db: Session):
    return db.query(models.thithili_unit).all()

def store_data_in_db( db: Session,data: List[dict]):
        
    for row in data:
            new_record = State_details(
                stateCode=row['stateCode'],
                stateName=row['stateName'],
                districtCode=row['districtCode'],
                districtName=row['districtName'],
                subdistrictCode=row['subdistrictCode'],
                subdistrictName=row['subdistrictName'],
                villageCode=row['villageCode'],
                villageName=row['villageName'],
                pincode=row['pincode'],
                shortName=row['shortname']
            )
            db.add(new_record)

            # Commit the transaction
    db.commit()
def get_by_state_pincode(db: Session, pincode: str):
    return db.query(models.State_details).filter(models.State_details.pincode == pincode).first()
def get_by_unit_pincode(db: Session, pincode: str):
    print("get by unit pincode")
    return db.query(models.thithili_unit).filter(models.thithili_unit.unitPinCode == pincode).order_by(models.thithili_unit.unit_id.desc()).first()

def store_unit_data(db: Session, unit_data: schemas.UnitCreate,unitCode):
    
    try:
        # Convert the unit data to a Unit model
        new_unit = models.thithili_unit(
            unitName=unit_data.unitName,
            unitCode=unitCode,
            unitArea=unit_data.unitArea,
            unitAddress=unit_data.unitAddress,
            unitPinCode=unit_data.unitPinCode,
            unitPatronsId=unit_data.unitPatronsId,
            unitEstablishedOn=unit_data.unitEstablishedOn,
            unitLogo=unit_data.unitLogo,
            unitLatitude=unit_data.unitLatitude,
            unitLongitude=unit_data.unitLongitude,
            createdBy=unit_data.createdBy,
            createdOn=unit_data.createdOn
        )
        
        # Add the unit to the session and commit
        db.add(new_unit)
        db.commit()
        db.refresh(new_unit)
        return new_unit

    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise ValueError(f"Error while saving unit data: {str(e)}")