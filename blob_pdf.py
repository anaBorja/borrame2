import os
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
from dotenv import load_dotenv

load_dotenv()

# Parámetros de conexión
conn_str =os.getenv("AZURE_STORAGE_CONNECTION_STRING")  # Sustituye con tu connection string
container_name = "pdf"  # Nombre del contenedor en Azure Blob Storage
folder_name = "computerdata/"  # Carpeta dentro del contenedor donde están los archivos

"""
# Configuración de Azure Blob Storage
azure_storage = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "pdf"
FOLDER_NAME = "computerdata/"
"""
# Crear el cliente del servicio de blobs
blob_service_client = BlobServiceClient.from_connection_string(conn_str)
container_client = blob_service_client.get_container_client(container_name)

# Directorio local para guardar los archivos
local_folder = "contenedordpf"

# Asegurarnos de que la carpeta local existe
if not os.path.exists(local_folder):
    os.makedirs(local_folder)

# Descargar los archivos .pdf.labels.json
for blob in container_client.list_blobs(name_starts_with=folder_name):
    blob_name = blob.name
    if blob_name.endswith('.pdf.labels.json'):
        # Obtener el cliente del blob
        blob_client = container_client.get_blob_client(blob_name)
        
        # Descargar el blob
        try:
            print(f"Descargando: {blob_name}...")
            download_path = os.path.join(local_folder, os.path.basename(blob_name))  # Nombre del archivo local
            with open(download_path, "wb") as file:
                blob_client.download_blob().readinto(file)
            print(f"Archivo guardado en: {download_path}")
        except ResourceNotFoundError:
            print(f"⚠️ Error: No se encontró el archivo {blob_name}")
        except Exception as e:
            print(f"❌ Error al descargar el archivo {blob_name}: {e}")

print("🚀 Proceso completado.")
