import os
import json
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

# Cargar el archivo .env
load_dotenv()

# Obtener la cadena de conexión desde el archivo .env
cosmosdb_conn = os.getenv("COSMOSDB_CONNECTION_STRING")
DB_NAME = "OrdenadoresDB"
COLLECTION_NAME = "ordenadores"

# Función para conectar con Cosmos DB usando MongoAPI
def obtener_cliente_cosmosdb():
    # Usar la conexión desde la variable de entorno
    cliente = MongoClient(cosmosdb_conn)
    return cliente

# Ruta de la carpeta donde están los archivos JSON
input_folder = "json_folder"  # Carpeta con los archivos JSON

# Conectar con Cosmos DB
cliente_cosmosdb = obtener_cliente_cosmosdb()

# Base de datos y colección de destino en Cosmos DB
db = cliente_cosmosdb[DB_NAME]
coleccion = db[COLLECTION_NAME]

# Función para cargar los archivos JSON en Cosmos DB
def cargar_archivos_en_cosmosdb(input_folder, coleccion):
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            input_file_path = os.path.join(input_folder, filename)
            
            # Leer el archivo JSON
            with open(input_file_path, 'r') as file:
                data = json.load(file)
            
            # Asegurarse de que cada documento tiene un ID único
            if '_id' not in data:
                data['_id'] = str(ObjectId())  # Crear un ObjectId si no existe
            
            # Insertar el documento en Cosmos DB
            coleccion.insert_one(data)
            
            print(f"Archivo {filename} cargado en Cosmos DB")

# Cargar todos los archivos en la carpeta
cargar_archivos_en_cosmosdb(input_folder, coleccion)
