from typing import Dict, Optional
from pydantic import BaseModel
from datetime import date, datetime

class UserProfileCreate(BaseModel):
    fullName: str
    aadhaarNumber: str
    gender: str 
    dateOfBirth: date
    mobileNumber: str
    fatherName: str 
    fatherMobile: str 
    motherName: str 
    motherMobile: str
    dateOfJoin: date
    address: str 
    area: str
    pinCode: str 
    profileAvatar: Optional[str] = None
    createdBy: str 
    createdOn: str
    latitude:str
    longitude:str
    motherAadhaar:str
    fatherAdhaar:str
    updatedBy: Optional[int] = None
    updatedOn: Optional[datetime] = None

    class Config:
        orm_mode = True
class StateDetailsCreate(BaseModel):
    stateCode: str
    stateName: str
    districtCode: str
    districtName: str
    subdistrictCode: str
    subdistrictName: str
    villageCode: str
    villageName: str
    pincode: str
    shortName:str

    class Config:
        orm_mode = True
        
class UnitCreate(BaseModel):
    unitName: str
    unitArea: str
    unitAddress: str
    unitPinCode: str
    unitPatronsId: str  # Assuming it's a comma-separated string of patron IDs
    unitEstablishedOn: str
    unitLogo: Optional[str] = None  # URL or path to the logo image
    unitLatitude: str
    unitLongitude: str
    createdBy: str
    createdOn: str
    updatedBy: Optional[str] = None
    updatedOn: Optional[str] = None

    class Config:
        orm_mode = True
