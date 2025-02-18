from pymongo import MongoClient
from azure.ai.language.conversations import ConversationAnalysisClient
from azure.core.credentials import AzureKeyCredential
from botbuilder.core import TurnContext, MessageFactory
import os

# Verificar si las variables están cargadas correctamente
language_key = os.getenv("LANGUAGE_SERVICE_KEY")
language_endpoint = os.getenv("LANGUAGE_SERVICE_ENDPOINT")

print(f"language_key: {language_key}")  # Verifica que la clave no sea None
print(f"language_endpoint: {language_endpoint}")  # Verifica que el endpoint esté correcto

if language_key is None or language_endpoint is None:
    print("¡ERROR! Las variables de entorno no se han cargado correctamente.")
else:
    from azure.ai.language.conversations import ConversationAnalysisClient
    from azure.core.credentials import AzureKeyCredential

    # Cliente de Azure Language
    language_client = ConversationAnalysisClient(language_endpoint, AzureKeyCredential(language_key))

    # Ahora puedes continuar con tu código
    print("Cliente de Azure Language creado correctamente.")


# Configuración de Language Studio
language_endpoint = os.getenv("LANGUAGE_SERVICE_ENDPOINT")
language_key = os.getenv("LANGUAGE_SERVICE_KEY")
print(f"language_key: {language_key}")
project_name = "computerbotclu"
deployment_name = "chatcomputer"

# Configuración de Cosmos DB (MongoDB API)
cosmos_endpoint = os.getenv("COSMOSDB_CONNECTION_STRING")

# Crear el cliente de MongoDB
client = MongoClient(cosmos_endpoint)

# Seleccionar la base de datos y colección
database = client.get_database("computerbot")
container = database.get_collection("ordenadores")

# Cliente de Language Service
language_client = ConversationAnalysisClient(language_endpoint, AzureKeyCredential(language_key))

async def handle_user_message(turn_context: TurnContext):
    user_input = turn_context.activity.text

    # Analizar la pregunta del usuario
    result = language_client.analyze_conversation(
        task={
            "kind": "Conversation",
            "analysisInput": {
                "conversationItem": {
                    "participantId": "user",
                    "text": user_input,
                    "id": "1"
                }
            },
            "parameters": {
                "projectName": project_name,
                "deploymentName": deployment_name,
                "stringIndexType": "TextElement_V8"
            }
        }
    )

    # Extraer intención y entidades
    intent = result["result"]["prediction"]["topIntent"]
    entities = {e["category"]: e["text"] for e in result["result"]["prediction"]["entities"]}

    # Construir la consulta a MongoDB
    query = {}
    for key, value in entities.items():
        query[key] = value

    # Ejecutar la consulta
    items = container.find(query)

    # Mostrar los resultados al usuario
    await send_results_to_user(turn_context, list(items))

async def send_results_to_user(turn_context: TurnContext, results):
    if results:
        message = "Aquí tienes los ordenadores que coinciden con tu búsqueda:\n"
        for item in results:
            message += f"- Modelo: {item['modelo']}, Procesador: {item['procesador']}, Memoria RAM: {item['memoria_ram']}, Precio: {item['precio']}\n"
    else:
        message = "No se encontraron ordenadores que coincidan con tu búsqueda."

    await turn_context.send_activity(MessageFactory.text(message))

print(f"language_key: {language_key}")  # Verifica que la clave es correcta y no es None o vacía
