import streamlit as st
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import re

# Cargar variables de entorno desde .env
load_dotenv()

# Conectar a Cosmos DB
connection_string = os.getenv("COSMOSDB_CONNECTION_STRING")
client = MongoClient(connection_string)
db = client["computerbot"]
collection = db["ordenadores"]

# Función para buscar en Cosmos DB
def buscar_en_cosmos_db(consulta):
    return collection.find(consulta)

# Función para preparar la respuesta
def preparar_respuesta(doc):
    return (
        f"Encontré un ordenador que podría interesarte:\n\n"
        f"**Marca**: {doc.get('marca', 'Desconocida')}\n"
        f"**Modelo**: {doc.get('modelo', 'Desconocido')}\n"
        f"**Sistema Operativo**: {doc.get('sistema operativo', 'Desconocido')}\n"
        f"**Procesador**: {doc.get('procesador', 'Desconocido')}\n"
        f"**Memoria RAM**: {doc.get('memoria ram', 'Desconocida')}\n"
        f"**Almacenamiento**: {doc.get('almacenamiento', 'Desconocido')}\n"
        f"**Tarjeta Gráfica**: {doc.get('tarjeta grafica', 'Desconocida')}\n"
        f"**Peso**: {doc.get('peso', 'Desconocido')}\n"
        f"**Precio**: {doc.get('precio', 'Desconocido')}\n"
        f"**Garantía**: {doc.get('garantia', 'Desconocida')}\n"
    )

# Interfaz de usuario con Streamlit
st.title("Chatbot de Búsqueda de Ordenadores")

# Entrada del usuario
user_message = st.text_input("Escribe tu búsqueda (por ejemplo, 'Lenovo con 16 GB de RAM'): ")

# Lógica de búsqueda
if user_message:
    consulta = {}
    
    if re.search(r"Lenovo", user_message, re.IGNORECASE):
        consulta["marca"] = "Lenovo"
    
    if re.search(r"(\d+ GB de RAM)", user_message, re.IGNORECASE):
        memoria = re.search(r"(\d+ GB de RAM)", user_message, re.IGNORECASE).group(1)
        consulta["memoria ram"] = memoria
    
    if re.search(r"(i7|i5|i9)", user_message, re.IGNORECASE):
        procesador = re.search(r"(i7|i5|i9)", user_message, re.IGNORECASE).group(1)
        consulta["procesador"] = procesador

    resultados = buscar_en_cosmos_db(consulta)

    if resultados.alive:
        st.success("🔍 Resultados de la búsqueda:")
        for doc in resultados:
            st.write(preparar_respuesta(doc))
    else:
        st.error(f"❌ No se encontraron resultados para: {user_message}.")
else:
    st.info("¡Hola! Puedo ayudarte a buscar ordenadores. Por ejemplo, escribe 'Lenovo con 16 GB de RAM'.")
