from sqlalchemy.orm import Session
from backend.database import  get_db
from backend.models.token_model import Token as TokenModel
from backend.schemas.doctor_department_schema import DoctorDepartment as DoctorDepartmentSchema
from fastapi import APIRouter,Depends, HTTPException, status
import datetime
from sqlalchemy import or_
router = APIRouter()


@router.get("/generate_tkn")
def list_departments_doctor(department:str,doctor:str, db:Session= Depends(get_db), status_code = status.HTTP_200_OK):
    try:
        query =  db.query(TokenModel).filter(TokenModel.diagonsed != 1, TokenModel.department == department,TokenModel.doctor == doctor)
        res= query.count()
        print(res)
        token = f'{department[0]}-{"".join([x[0] for x in doctor.split(" ")])}-{str(res+1)}'
        return {"token":token}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/reset_tkn")
def reset_token(doctor:str, db:Session=Depends(get_db), status_code = status.HTTP_200_OK):
    try:
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        tmrw = (datetime.datetime.today()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        query =  db.query(TokenModel).filter(TokenModel.doctor == doctor, TokenModel.created_time.between(today,tmrw) )
        print(query)
        print(query.all())
        query.update({TokenModel.diagonsed:1}, synchronize_session=False)
        db.commit()
        return {"message":"Success"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/waiting_time")
def reset_waiting_time(token:str, db:Session=Depends(get_db)):
    try:
        if token == "" or token == None:
            raise Exception()
        token_condition = f"{'-'.join(token.split('-')[:2])}%"
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        tmrw = (datetime.datetime.today()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        query = db.query(TokenModel.token).filter( TokenModel.token.like(token_condition),TokenModel.created_time.between(today,tmrw))
        res = query.count()
        return {"waitingTime":f"{res*10}"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/token_status")
def getTokenStatus(token:str, db:Session=Depends(get_db)):
    try:
        query = db.query(TokenModel.diagonsed).filter( TokenModel.token == token)
        return {"status":f"{query.first()[0]}"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/get_patients")
def get_patients(doctor:str, db:Session=Depends(get_db), status_code = status.HTTP_200_OK):
    try:
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        tmrw = (datetime.datetime.today()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        query = db.query(TokenModel).filter(TokenModel.doctor == doctor,TokenModel.created_time.between(today,tmrw))
        if query.first() is not None:
            return {"details":  query.all()}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)