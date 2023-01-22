from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.database import  get_db
from backend.models.department_doctor_model import DoctorDepartment as DoctorDepartmentModel
from backend.models.token_model import Token as TokenModel
from backend.schemas.doctor_department_schema import DoctorDepartment as DoctorDepartmentSchema
from fastapi import APIRouter,Depends, HTTPException, status, Response

router = APIRouter()


@router.get("/list/departments")
def list_departments(db:Session= Depends(get_db), status_code = status.HTTP_200_OK):
    try:
        res =  db.query(DoctorDepartmentModel.department.distinct().label('department')).all()
        reponse = {"Departments":[x.department for x in res]}
        return reponse
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/list/doctors")
def list_departments_doctor(department:str, db:Session= Depends(get_db), status_code = status.HTTP_200_OK):
    try:
        res =  db.query(DoctorDepartmentModel.doctor.distinct().label('doctor')).filter(DoctorDepartmentModel.department == department).all()
        reponse = {"Doctors":[x.doctor for x in res]}
        return reponse
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.put("/select_doctor")
def list_departments_doctor(department:str,doctor:str, next_token:str, db:Session= Depends(get_db), status_code = status.HTTP_200_OK):
    message = "Token Success"
    try:
        res =  db.query(TokenModel).filter(TokenModel.department == department,TokenModel.doctor == doctor, TokenModel.diagonsed != 1).count()
        token = f'{department[0]}-{"".join([x[0] for x in doctor.split(" ")])}-{str(res+1)}'
        if token == next_token or res == 0:

            token_data = TokenModel(doctor=doctor,department=department,diagonsed=-1,token=token)
            db.add(token_data)
            db.commit()
            response = {"token": token, "message": message}
            return response
        elif res is int(next_token[-1]):
            message= "Token Already Present"
        else:
            print(res, next_token[-1])
            message = "Bad Token"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    
@router.get("/next_patient")
def call_next_patient(token:str,doctor:str, department:str, db:Session=Depends(get_db), status_code = status.HTTP_200_OK):
    try:
        query = db.query(TokenModel).filter(TokenModel.diagonsed == -1, TokenModel.doctor == doctor, TokenModel.department == department)
        query = query.order_by(TokenModel.token.asc())
        res= query.first()
        if res is not None:
            if int(res[-1])-1 is int(token[-1]):
                return {"next_token":res}
            else:
                print("Here")
                raise Exception()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No New Patient")

@router.put("/consulting")
def update_consulting_status(token:str, db:Session=Depends(get_db), status_code = status.HTTP_200_OK):
    try:
        query = db.query(TokenModel).filter(TokenModel.token == token)
        if query.first() is not None:
            query.update({TokenModel.diagonsed:0}, synchronize_session=False)
            db.commit()
            return {"Message": "Consulting"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Wrong token")

@router.put("/diagonsed")
def update_diagonsed(token:str, db:Session=Depends(get_db), status_code = status.HTTP_200_OK):
    try:
        query = db.query(TokenModel).filter(TokenModel.token == token)
        if query.first() is not None:
            query.update({TokenModel.diagonsed:1}, synchronize_session=False)
            db.commit()
            return {"Message": "Success"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Wrong token")

@router.put("/add_doctor")
def add_doctor(department:str, doctor:str, response:Response,db:Session=Depends(get_db), status_code = status.HTTP_200_OK):
    try:
        query = db.query(DoctorDepartmentModel).filter(DoctorDepartmentModel.doctor == doctor, DoctorDepartmentModel.department == department)
        if query.count() >0:
            response.status_code = status.HTTP_409_CONFLICT
            return {"Message": "Doctor with that name is already exists"}
        else:
            db.add(DoctorDepartmentModel(doctor=doctor, department=department))
            db.commit()
            return {"Message": "Success"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)




