from models.update_models import ClienteCreado, UpdateIn
from db.cliente_db import ClienteInDB, get_cliente, usuarios_db
from models.user_models import ClienteIn, ClienteOut
import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


hotel = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://reserva-hotel-appvue.herokuapp.com"
]

hotel.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


@hotel.get("/") #carpeta raiz del sitio                                        
async def home():   # funcion home asíncrona
    return {"message": "Sistema de reservas hotel"} # muestra un mensaje en la carpeta raiz del sitio

@hotel.post("/cliente/auth")
async def auth_user(cliente_ingresado: ClienteIn):

    cliente_en_bd = get_cliente(cliente_ingresado.username)
    

    if cliente_en_bd == None:      # si la variable está vacía (quiere decir que user_in_db tambien lo está, porque el usuario al que se intenta acceder no está en la base de datos)
        raise HTTPException(status_code=404, detail="El usuario no existe")

    if cliente_ingresado.contrasena != cliente_en_bd.contrasena:
        return {"Cliente autenticado": False}

    return {"Autenticado": True} # si quiero mostrar solo el email y el celular


@hotel.get("/cliente/info/{cliente_ingresado}")
async def get_info_cliente(cliente_ingresado: str):

    cliente_en_bd = get_cliente(cliente_ingresado)

    if cliente_en_bd == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    cliente_out = ClienteOut(**cliente_en_bd.dict())
    
    return cliente_out

@hotel.put("/cliente/update")
async def update_info_cliente(cliente_ingresado: UpdateIn):

    cliente_en_bd = get_cliente(cliente_ingresado.username)

    if cliente_en_bd == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    
    cliente_en_bd.username = cliente_ingresado.username
    cliente_en_bd.telefono = cliente_ingresado.telefono
    cliente_en_bd.email = cliente_ingresado.email

    return {"Actualizado": True}
        
@hotel.get("/cliente/all")
async def show_all_users():
    return usuarios_db

###############################################
###############################################
# CREAR CLIENTE ##############################
##############################################

@hotel.put("/crear-cliente")
async def crear_cliente(cliente_ingresado: ClienteCreado):

    cliente_en_bd = get_cliente(cliente_ingresado.username)

    if(cliente_en_bd != None ):
        
        
        
        return {"Cliente-creado": True}

    
    return {"Cliente-creado": False}


#@hotel.get("/user/")

# uvicorn main:hotel --reload


