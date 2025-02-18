from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from pymongo import MongoClient
import os

class ComputerBot(ActivityHandler):
    def __init__(self):
        # Conexión a Cosmos DB
        self.connection_string = os.getenv("COSMOSDB_CONNECTION_STRING")
        self.client = MongoClient(self.connection_string)
        self.db = self.client["computerbot"]
        self.collection = self.db["ordenadores"]

    async def on_message_activity(self, turn_context: TurnContext):
        user_message = turn_context.activity.text.lower()

        # Lógica de búsqueda en Cosmos DB
        if "buscar" in user_message:
            # Extraer la característica de búsqueda (por ejemplo, "memoria ram 16 GB")
            search_term = user_message.replace("buscar", "").strip()

            # Buscar en Cosmos DB
            resultados = self.collection.find({"entidades.memoria_ram": search_term})

            # Preparar la respuesta
            if resultados.count() > 0:
                response = "🔍 Resultados de la búsqueda:\n"
                for doc in resultados:
                    response += f"- {doc['entidades']['marca']} {doc['entidades']['modelo']} ({doc['entidades']['memoria_ram']})\n"
            else:
                response = "❌ No se encontraron resultados."

            # Enviar la respuesta al usuario
            await turn_context.send_activity(MessageFactory.text(response))
        else:
            await turn_context.send_activity(MessageFactory.text("¡Hola! Puedo ayudarte a buscar ordenadores. Por ejemplo, escribe 'buscar memoria ram 16 GB'."))
async def on_message_activity(self, turn_context: TurnContext):
    user_message = turn_context.activity.text.lower()

    if "buscar" in user_message:
        search_term = user_message.replace("buscar", "").strip()

        # Determinar la categoría de búsqueda
        if "marca" in search_term:
            categoria = "marca"
            valor = search_term.replace("marca", "").strip()
        elif "procesador" in search_term:
            categoria = "procesador"
            valor = search_term.replace("procesador", "").strip()
        elif "memoria ram" in search_term:
            categoria = "memoria_ram"
            valor = search_term.replace("memoria ram", "").strip()
        elif "almacenamiento" in search_term:
            categoria = "almacenamiento"
            valor = search_term.replace("almacenamiento", "").strip()
        else:
            await turn_context.send_activity(MessageFactory.text("❌ No entendí la búsqueda. Intenta con 'buscar marca Lenovo' o 'buscar memoria ram 16 GB'."))
            return

        # Buscar en Cosmos DB
        resultados = self.collection.find({f"entidades.{categoria}": valor})

        # Preparar la respuesta
        if resultados.count() > 0:
            response = f"🔍 Resultados de la búsqueda ({categoria} = {valor}):\n"
            for doc in resultados:
                response += f"- {doc['entidades']['marca']} {doc['entidades']['modelo']} ({doc['entidades'][categoria]})\n"
        else:
            response = f"❌ No se encontraron resultados para {categoria} = {valor}."

        # Enviar la respuesta al usuario
        await turn_context.send_activity(MessageFactory.text(response))
    else:
        await turn_context.send_activity(MessageFactory.text("¡Hola! Puedo ayudarte a buscar ordenadores. Por ejemplo, escribe 'buscar marca Lenovo' o 'buscar memoria ram 16 GB'."))