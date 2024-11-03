from fastapi import FastAPI, HTTPException, Query, Path
from typing import List, Optional
from database import container_proyectos, container_usuarios
from models import Proyecto, Usuario
from azure.cosmos import exceptions
from datetime import datetime

app = FastAPI(title='API de Gestion de usuarios y proyectos')
 
#### Endpoint de usuarios
 
@app.get("/")

def home():

    return "Hola Mundo"
 
# Crear usuario

@app.post("/usuarios/", response_model=Usuario, status_code=201)

def create_event(usuario: Usuario):

    try:

        container_usuarios.create_item(body=usuario.dict())

        return usuario

    except exceptions.CosmosResourceExistsError:

        raise HTTPException(status_code=400, detail="El evento con este ID ya existe.")

    except exceptions.CosmosHttpResponseError as e:

        raise HTTPException(status_code=400, detail=str(e))
 

 
 
# Listar usuarios

@app.get("/usuarios/", response_model=List[Usuario])

def list_envent():

    query = "SELECT * FROM c WHERE 1=1"

    items = list(container_usuarios.query_items(query=query, enable_cross_partition_query=True))

    return items
 
# Actualizar usuarios

@app.put("/usuarios/{usuario_id}", response_model=Usuario)

def update_usuario(usuario_id: str, updated_usuario: Usuario):
 
    try:

        usuario = container_usuarios.read_item(item=usuario_id, partition_key=usuario_id)

        # Actualizar campos

        usuario.update(updated_usuario.dict(exclude_unset=True))

       
        container_usuarios.replace_item(item=usuario_id, body=usuario)

        return usuario

    except exceptions.CosmosResourceNotFoundError:

        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    except exceptions.CosmosHttpResponseError as e:

        raise HTTPException(status_code=400, detail=str(e))
 
# Eleimar usuario
 
@app.delete("/usuarios/{usuario_id}", status_code=204)

def delete_usuario(usuario_id: str):

    try:

        container_usuarios.delete_item(item=usuario_id, partition_key=usuario_id)

        return

    except exceptions.CosmosResourceNotFoundError:

        raise HTTPException(status_code=404, detail='Evento no encotrado')

    except exceptions.CosmosHttpResponseError as e:

        raise HTTPException(status_code=400, detail=str(e))


#Endpoints de proyectos

# Listar proyectos
@app.get("/proyectos/", response_model=List[Proyecto])
def list_projects():
   
    query = "SELECT * FROM c WHERE 1=1"
    proyectos = list(container_proyectos.query_items(query=query, enable_cross_partition_query=True))
    return proyectos
 
 
# Crear proyecto
@app.post("/proyectos/", response_model=Proyecto, status_code=201)
def add_project(proyecto: Proyecto):
    try:
        usuario = container_usuarios.read_item(item=proyecto.id_usuario, partition_key=proyecto.id_usuario)
        if not usuario: 
            raise  HTTPException(status_code=404, detail="El usuario con este ID no existe")
 
        container_proyectos.create_item(body=proyecto.dict())
        return proyecto
    except exceptions.CosmosResourceExistsError:
        raise HTTPException(status_code=400, detail="El proyecto con este ID ya existe.")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))
 
 
# Obtener proyectos por usuario
@app.get("/usuarios/{usuario_id}/proyectos",response_model=List[Proyecto])
def proyecto_por_usuario(usuario_id: str):
 
    try:
 
        query = f"SELECT * FROM c WHERE c.id_usuario='{usuario_id}'"
        items = list(container_proyectos.query_items(query=query, enable_cross_partition_query=True))
        return items
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="El usuario con este ID no existe")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))


#ACtualizar proyecto
@app.put("/proyectos/{proyecto_id}", response_model=Proyecto)
def update_proyecto(proyecto_id: str, updated_proyecto: Proyecto):
 
    try:
        proyecto = container_proyectos.read_item(item = proyecto_id, partition_key = proyecto_id)
 
        usuario = container_usuarios.read_item(item = updated_proyecto.id_usuario, partition_key = updated_proyecto.id_usuario)

        if updated_proyecto.id_usuario != proyecto['id_usuario']:
            raise HTTPException(status_code=404, detail="El usuario no puede modificar informacion de este proyecto")
 
        proyecto.update(updated_proyecto.dict(exclude_unset=True))
        container_proyectos.replace_item(item=updated_proyecto, body=proyecto)
 
        return proyecto
 
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Proyecto no encontrado')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))
       
 
# Eliminar proyecto por id
@app.delete("/proyectos/{proyecto_id}", status_code=204)
def delete_project(proyecto_id: str):
    try:
        # Si el proyecto no existe lanza un CosmosResourceNotFoundError
        container_proyectos.delete_item(item = proyecto_id, partition_key = proyecto_id)
        return
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Proyecto no encontrado')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))
 