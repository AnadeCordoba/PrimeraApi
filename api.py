#Importación librerías que vamos a utilizar
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd

# función para leer el dataset
def dataset():
    df = pd.read_csv("iris_dataset.csv")
    return pd.DataFrame(df)

#Se crea una clase con BaseModel para saber la estructura, nombre de las columnas y los datos que utiliza. 
# ¡¡¡SIN COMAS!!!!
class Flor(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    species: str

#Creamos variable para llamar a FastApi
app = FastAPI()

#Primera parte. 
# Llamamos a raiz
@app.get('/')
#Definimos una función para que nos haga un return del JSON pedido. ¡¡Mejor en asincrono!!
async def mensaje():
    return {"mensaje":"¡¡Buenos días!!"}

# GET Para IrisDataset 
@app.get('/iris')
#Creo una función para Iris
async def iris_get():
    df = dataset()
    #JSONResponse devuelve en formato JSON y asi es como se puede modificar.
    return JSONResponse(content= df.to_dict())


# ASI ME COMPLICO LA VIDA CON LAS FLORES

#Post para Iris
@app.post('/iris')
#creo una funcion para Iris post y llamo a la clase en los atributos
async def iris_post(miflor:Flor):
    #hay que leer el df para saber que vamos a trabajar con eso
    df=dataset()
    #hago una serie de pandas y uno con los parametros de la clase
    florecitas = pd.Series([miflor.sepal_length,miflor.sepal_width,miflor.petal_length,miflor.petal_width,miflor.species], index=df.columns)
    df = df.append(florecitas,ignore_index=True) #es el metodo para introducir nuevos datos
    #Tenemos que llamar al csv para que se guarde
    df.to_csv('iris_dataset.csv')
    return JSONResponse(content= df.to_dict())


# Delete para iris se ponen las llaves {} para que en la ruta no aparezca la interrogación.
@app.delete('/iris/{fila}')
# Funcion para Iris delete, en los parametros como quiero eliminar por el numero de fila, le pongo en el parametro por lo que quiero borrar y el valor que va a recibir.
async def iris_delete(fila:int):
    # Hay que leer el df para saber que se trabaja con el.
    df = dataset()
    df =df.drop(fila) # se pone inplace=true cuando no lo has guardado en una variable
    #se vuelve a llamar al df para que se guarde.
    df.to_csv('iris_dataset.csv')
    return JSONResponse(content= df.to_dict())

#Put para iris
@app.put('/iris')
#Funcion para iris put, en los parametros pongo de donde voy a coger los datos (clase) y la fila para que lo busque. Es una mezcla de post y delete.
async def iris_put(miflor:Flor, fila:int):
    df =dataset()
    #para poder modificar los valores utilizo .loc para que sea en orden
    df.loc[fila,['sepal_length']] = miflor.sepal_length
    df.loc[fila,['sepal_width']] = miflor.sepal_width
    df.loc[fila,['petal_length']] = miflor.petal_length
    df.loc[fila,['petal_width']] = miflor.petal_width
    df.loc[fila,['species']] = miflor.species
    #se llama al csv para que guarde los datos
    df.to_csv('iris_dataset.csv')
    return JSONResponse(content= df.to_dict())

# PATCH para iris
@app.patch('/iris')
async def iris_patch():
    return