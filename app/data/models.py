import uuid
from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from .database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    
    # UUID as an additional unique identifier
    user_id = Column(String,primary_key=True, nullable=False, default=lambda: str(uuid.uuid4()).replace("-", ""))
    fullName = Column(String(255), nullable=False)
    aadhaarNumber = Column(String(255),unique=False, index=True) # Allow duplicates for versioning
    motherAadhaar=Column(String(255))
    fatherAdhaar=Column(String(255))
    gender = Column(String(10))
    dateOfBirth = Column(Date, nullable=False)
    mobileNumber = Column(String(12), nullable=False)
    fatherName = Column(String(255))
    fatherMobile = Column(String(255))
    motherName = Column(String(255))
    motherMobile = Column(String(10))
    dateOfJoin = Column(Date, nullable=False)
    address = Column(String(255))
    area = Column(String(255))
    pinCode = Column(String(20))
    profileAvatar = Column(String(255))
    createdBy = Column(String(255),nullable=True)
    createdOn = Column(String(255))
    latitude=Column(String(255))
    longitude=Column(String(255))
    updatedBy = Column(String(15), nullable=True)  # Nullable for new records
    updatedOn = Column(String(50), nullable=True)  # Nullable for new records
        # Foreign key to thithili_unit
    unitCode= Column(String, ForeignKey('thithili_unit.unitCode'), nullable=True)
    
    # Relationship to the ThithiliUnit model (one-to-many relationship)
    unit = relationship("thithili_unit", backref="users")
    

class State_details(Base):
    __tablename__ = "state_details"
        # Define the columns in the table
    id = Column(Integer, primary_key=True, index=True)
    stateCode = Column(String(255))   # Adjust column types as per your data
    stateName = Column(String(255))
    districtCode = Column(String(50))
    districtName = Column(String(255))
    subdistrictCode = Column(String(50))
    subdistrictName = Column(String(255))
    villageCode = Column(String(50))
    villageName = Column(String(255))
    pincode = Column(String(50))
    shortName=Column(String(10))
    

    
class thithili_unit(Base):
    __tablename__ = "thithili_unit"
    
    # Define the columns in the table
    unit_id = Column(Integer, primary_key=True, autoincrement=True)  # Adding an auto-incremented ID as the primary key
    def formatted_unit_id(self):
        # Formatting the unit_id as a 4-digit zero-padded string
        return str(self.unit_id).zfill(4)
    unitCode=Column(String(500),unique=True)
    unitName = Column(String(255), nullable=False)
    unitArea = Column(String(255))
    unitAddress = Column(String(255))
    unitPinCode = Column(String(50))  # Assuming pincode will be a string (since it could have leading zeros)
    unitPatronsId = Column(String(255))  # A comma-separated string to store patron IDs
    unitEstablishedOn = Column(String(50))  # Date format (string can be converted to datetime)
    unitLogo = Column(String(255))  # URL or file path for the logo
    unitLatitude = Column(String(50))
    unitLongitude = Column(String(50))
    createdBy = Column(String(255))
    createdOn = Column(String(50))  # Assuming 'createdOn' is a timestamp (integer)

    
    
