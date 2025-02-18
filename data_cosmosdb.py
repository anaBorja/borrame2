import os
import json
from azure.storage.blob import BlobServiceClient
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Configuración de Azure Blob Storage
azure_storage = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "pdf"
FOLDER_NAME = "computerdata/"

# Configuración de CosmosDB MongoAPI
cosmosdb_conn = os.getenv("COSMOSDB_CONNECTION_STRING")
DB_NAME = "OrdenadoresDB"
COLLECTION_NAME = "CaracteristicasOrdenadores"

# Conectar a Azure Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(azure_storage)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# Conectar a CosmosDB
mongo_client = MongoClient(cosmosdb_conn)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

# Función para extraer los valores de las etiquetas
def extraer_texto_label(labels, nombre):
    # Recorremos las etiquetas y buscamos el texto asociado a la etiqueta
    for item in labels:
        if item.get("label") == nombre:
            # Devuelvo el texto si se encuentra
            if "text" in item:
                return item["text"]
    return None

# Procesar cada archivo en la carpeta 'computerdata/'
for blob in container_client.list_blobs(name_starts_with=FOLDER_NAME):
    # Filtrar solo archivos JSON
    blob_name = blob.name
    if not blob.name.endswith('.pdf.labels.json'):
        print(f"⏭️ Ignorado: {blob_name} (no es un archivo JSON)")
        continue  # Ignorar archivos que no sean JSON
    
    blob_client = container_client.get_blob_client(blob.name)
    
    try:
        blob_data = blob_client.download_blob().readall().decode("utf-8", errors="replace").strip()
        if not blob_data:
            print(f"⚠️ Archivo vacío: {blob.name}, se omite.")
            continue
        
        json_data = json.loads(blob_data)
        
        # Eliminar el campo "$schema" si está presente
        if "$schema" in json_data:
            del json_data["$schema"]

        # Extraer etiquetas del JSON
        labels = json_data.get("labels", [])

        print(f"Labels para el archivo {blob.name}: {labels}")

        # Extraer el _id del documento
        _id = json_data.get("document", "").strip()  # Usar 'document' como ID si existe

        # Si _id está vacío, usar el nombre del archivo como fallback
        if not _id:
            print(f"⚠️ El '_id' del archivo {blob.name} está vacío, se usará el nombre del archivo como ID.")
            _id = blob.name  # Usar el nombre del archivo como _id

        # Extraer 'codigo' de las etiquetas
        codigo = extraer_texto_label(labels, "codigo")
        
        # Si 'codigo' no se encuentra, se puede asignar un valor predeterminado
        if not codigo:
            print(f"⚠️ El campo 'codigo' no está presente en {blob.name}, se asignará un valor predeterminado.")
            codigo = "default_codigo"  # Valor predeterminado para 'codigo'

        # Construir el documento con la estructura deseada
        datos_procesados = {
            "_id": _id,
            "marca": extraer_texto_label(labels, "marca"),
            "modelo": extraer_texto_label(labels, "modelo"),
            "sistema operativo": extraer_texto_label(labels, "sistema operativo"),
            "procesador": extraer_texto_label(labels, "procesador"),
            "memoria ram": extraer_texto_label(labels, "RAM"),
            "almacenamiento": extraer_texto_label(labels, "almacenamiento"),
            "tarjeta grafica": extraer_texto_label(labels, "grafica marca"),
            "modelo grafica": extraer_texto_label(labels, "grafica modelo"),
            "peso": extraer_texto_label(labels, "peso"),
            "duracion": extraer_texto_label(labels, "duracion"),
            "codigo": codigo,  # Aseguramos que 'codigo' esté presente
            "precio": extraer_texto_label(labels, "precio"),
            "garantia": extraer_texto_label(labels, "garantia"),
            "disco duro": extraer_texto_label(labels, "disco duro"),
            "frecuencia procesador": extraer_texto_label(labels, "frecuencia procesador"),
            "pantalla": extraer_texto_label(labels, "tamaño"),
            "resolucion": extraer_texto_label(labels, "resolucion"),
            "altura": extraer_texto_label(labels, "altura"),
            "ancho": extraer_texto_label(labels, "ancho"),
            "color": extraer_texto_label(labels, "color"),
            "bluetooth": extraer_texto_label(labels, "bluetooth"),
            "equipo": extraer_texto_label(labels, "soluciones"),
            "puerto USB": extraer_texto_label(labels, "puerto USB"),
            "garantia modelo": extraer_texto_label(labels, "garantia modelo"),
            "material": extraer_texto_label(labels, "material")
        }

        # Eliminar claves con valores None
        datos_procesados = {k: v for k, v in datos_procesados.items() if v is not None}
        
        # Verificar que el _id no esté vacío
        if not datos_procesados["_id"]:
            print(f"⚠️ El '_id' está vacío para el archivo {blob.name}. Se omite.")
        else:
            try:
                # Insertar en CosmosDB
                collection.insert_one(datos_procesados)
                print(f"✅ Insertado: {blob.name}")
            except Exception as e:
                print(f"❌ Error al insertar {blob.name}: {str(e)}")

    except json.JSONDecodeError:
        print(f"❌ Error: Archivo {blob.name} no es un JSON válido, se omite.")

print("🚀 Proceso completado.")
