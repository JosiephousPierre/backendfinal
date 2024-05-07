# main.py
from fastapi import FastAPI
from model.manage import ManageRouter
from model.consult import ConsultRouter
from model.manage_med import MedicineRouter
from model.admin import AdminRouter
from model.manage_illness import IllnessRouter
from model.consulted_illness import ConsultedIllnessRouter
from model.consulted_med import ConsultedMedicationRouter
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI()

origins = [
    "http://localhost:5173",  # Allow localhost for development
     "https://stirring-frangollo-3f6016.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include CRUD routes from modules
app.include_router(ManageRouter, prefix="/api")
app.include_router(ConsultRouter, prefix="/api")
app.include_router(MedicineRouter, prefix="/api")
app.include_router(AdminRouter, prefix="/api")
app.include_router(IllnessRouter, prefix="/api")
app.include_router(ConsultedIllnessRouter, prefix="/api")
app.include_router(ConsultedMedicationRouter, prefix="/api")