from pymongo import MongoClient
import json
import os

# Cargar las variables de entorno desde .env
from dotenv import load_dotenv
load_dotenv()

# Obtener la cadena de conexión de Cosmos DB (MongoDB API)
connection_string = os.getenv("COSMOSDB_CONNECTION_STRING")
# Acceder a la base de datos y colección
database_name = "computerbot"  # Nombre de la base de datos
container_name = "ordenadores"  # Nombre de la colección

client = MongoClient(connection_string)

db = client[database_name]
collection = db[container_name]

# Ruta de la carpeta donde están los archivos JSON
output_directory = 'output_json_files4'

# Leer todos los archivos JSON en la carpeta y subirlos a Cosmos DB
for filename in os.listdir(output_directory):
    file_path = os.path.join(output_directory, filename)

    # Asegurarse de que es un archivo JSON
    if filename.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

            # Insertar el documento en Cosmos DB
            try:
                collection.insert_one(data)
                print(f"Documento insertado: {filename}")
            except Exception as e:
                print(f"Error al insertar el documento {filename}: {e}")
