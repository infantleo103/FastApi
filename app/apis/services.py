

from io import BytesIO
import logging
from typing import List

from fastapi import HTTPException
from data import media
from data import schemas
from data import crud
from sqlalchemy.orm import Session
import pyarrow.csv as pv_csv
from io import BytesIO

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

state_shortnames = {
    "kerala": "KL",
    "tamilnadu": "TN",
    "andhra pradesh": "AP",
    "uttar pradesh": "UP",
    "maharashtra": "MH",
    "karnataka": "KA",
    "bihar": "BR",
    "west bengal": "WB",
    "rajasthan": "RJ",
    "madhya pradesh": "MP",
    "gujarat": "GJ",
    "delhi": "DL",
    "haryana": "HR",
    "punjab": "PB",
    "odisha": "OD",
    "uttarakhand": "UK",
    "himachal pradesh": "HP",
    "assam": "AS",
    "jammu and kashmir": "JK",
    "chhattisgarh": "CG",
    "jharkhand": "JH",
    "goa": "GA",
    "tripura": "TR",
    "manipur": "MN",
    "meghalaya": "ML",
    "mizoram": "MZ",
    "nagaland": "NL",
    "sikkim": "SK",
    "arunachal pradesh": "AR",
    "andaman and nicobar islands": "AN",
    "lakshadweep": "LD",
    "dadra and nagar haveli and daman and diu": "DN",
    "puducherry": "PY"
}

def get_user(db: Session):
    get_data=crud.get_user(db=db)
    return get_data

def get_unit(db: Session):
    get_data=crud.get_(db=db)
    return get_data

def add_user(db: Session, user_to_add: List[schemas.UserProfileCreate]):
    print("printed query")
    # print(user_to_add.get("fullname"))
    added_user = crud.add_user(db, user_to_add)
    return added_user

# def add_unit(db: Session, unit_to_add):
#     print("Printed query")
#     unit_pincode=unit_to_add.unitPinCode
#     print("unit pincode",unit_pincode)
#     get_pincode=crud.get_by_state_pincode(db=db,pincode=unit_pincode)
#     print("get state pincode",get_pincode.pincode)
#     state_pincode=get_pincode.pincode
#     short_stateName=get_pincode.shortName
#     if unit_pincode== state_pincode:
#         data=crud.get_by_unit_pincode(db=db,pincode=unit_pincode)
#         try:
#             if data.unit_id:
#                 last_num = int(.unitCode[2:])  # Extract the number part from the last unit code
#                 new_num = last_num + 1
#             else:
#                 new_num = 1 
#         except:
#             unitCode=short_stateName+"0001"
    
#     added_unit = crud.store_unit_data(db, unit_to_add,unitCode)
#     return added_unit
def add_unit(db: Session, unit_to_add):
    # print("Printed query")
    unit_pincode = unit_to_add.unitPinCode

    get_pincode = crud.get_by_state_pincode(db=db, pincode=unit_pincode)
    
    state_pincode = get_pincode.pincode
    short_stateName = get_pincode.shortName
    
    if unit_pincode == state_pincode:
        data = crud.get_by_unit_pincode(db=db, pincode=unit_pincode)
        
        # Check if unit already exists and generate new unitCode
        try:
            if data and hasattr(data, 'unit_id') and data.unit_id:
                
                last_num = int(data.unitCode[2:])  
                new_num = last_num + 1
                unitCode = short_stateName + str(new_num).zfill(4) 
            else:
                unitCode = short_stateName + "0001" 
                
        except Exception as e:
            print("Error generating unit code:", e)
            unitCode = short_stateName + "0001"  
    
    # Store the new unit data
    added_unit = crud.store_unit_data(db, unit_to_add, unitCode)
    
    return added_unit




def delete_user(db, user_id) :
    print("printed query")
    # print(user_to_add.get("fullname"))
    deleted_user = crud.deleted_user(db, user_id)
    return deleted_user

def delete_unit(db, unit_code) :
    print("printed query")
    # print(user_to_add.get("fullname"))
    deleted_user = crud.deleted_units(db, unit_code)
    return deleted_user
    

def updated_user(db: Session, user_to_update: schemas.UserProfileCreate):
    """
    Creates a new row for user data, even if user data already exists.
    Instead of updating, creates a versioned record.
    """
    # Call the crud function to add a new version of the user
    print("updated query")
    adharnumber=user_to_update.aadhaarNumber
    image_profile=user_to_update.profileAvatar
    created_time=user_to_update.createdOn
    new_user_id = crud.update_user(db, user_to_update)
    log.info(f"Created new user record with ID: {new_user_id}")
    return new_user_id

def get_by_adhar_id(db: Session,adhar_id=id):
    return crud.get_by_adhar_id(db=db,adhar_id=adhar_id)


def get_by_pincode(db: Session,pincode=id):
    return crud.get_by_adhar_id(db=db,adhar_id=pincode)


def process_csv_data(file_content: bytes, db: Session):
    try:
        # Convert the file content to a BytesIO object
        buffer = BytesIO(file_content)

        # Using PyArrow to read the CSV into a Table
        table = pv_csv.read_csv(buffer)

        # Convert PyArrow Table to a Pandas DataFrame and then to a list of dictionaries
        rows = table.to_pandas().to_dict(orient='records')

        # Rename columns as per your requirement and add the 'shortname' column
        renamed_rows = []
        for row in rows:
            state_name = row['stateNameEnglish'].lower()

            # Get the shortname from the mapping, defaulting to None if not found
            shortname = state_shortnames.get(state_name, None)

            renamed_row = {
                'stateCode': row['stateCode'],
                'stateName': row['stateNameEnglish'],
                'districtCode': row['districtCode'],
                'districtName': row['districtNameEnglish'],
                'subdistrictCode': row['subdistrictCode'],
                'subdistrictName': row['subdistrictNameEnglish'],
                'villageCode': row['villageCode'],
                'villageName': row['villageNameEnglish'],
                'pincode': row['pincode'],
                # Adding shortname based on stateName
                'shortname': shortname
            }
            renamed_rows.append(renamed_row)
        
        print("Renamed Data with shortnames:", renamed_rows)

        # Call the crud function to store data in the database
        return crud.store_data_in_db(data=renamed_rows, db=db)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV data: {str(e)}")