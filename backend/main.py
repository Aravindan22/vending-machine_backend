from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import   engine, Base
from backend.models.token_model import Token

from backend.routes.doctor_department import router as dc_route
from backend.routes.token import router as tk_route

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(dc_route)
app.include_router(tk_route)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def ping():
    return { "pong": "Hello World"}


"""
CREATE TABLE `doctor_department` (
	`doctor` varchar(100) NOT NULL,
	`department` varchar(100) NOT NULL,
	PRIMARY KEY (`doctor`)
) ENGINE InnoDB,
  CHARSET utf8mb4,
  COLLATE utf8mb4_0900_ai_ci;


CREATE TABLE `token` (
	`id` int NOT NULL AUTO_INCREMENT,
	`doctor` varchar(100),
	`department` varchar(100) NOT NULL,
	`token` varchar(12) NOT NULL,
	`diagonsed` int NOT NULL,
	`created_time` datetime,
	PRIMARY KEY (`id`)
) ENGINE InnoDB,
  CHARSET utf8mb4,
  COLLATE utf8mb4_0900_ai_ci;

"""