import json
import os

# Ruta del archivo JSON de NER
input_json_file = 'computerbot(chatcomputer).json'

# Directorio donde se guardarán los archivos JSON generados
output_directory = 'output_json_files4'

# Crear la carpeta de salida si no existe
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Función para leer el contenido del archivo de texto
def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Leer el archivo JSON original
with open(input_json_file, 'r', encoding='utf-8') as file:
    ner_data = json.load(file)

# Función para crear un JSON con la información procesada
def process_ner_data(ner_data):
    for document in ner_data['assets']['documents']:
        # Obtener el nombre del archivo (el código de producto)
        document_location = document['location']
        file_name = os.path.basename(document_location).replace('.txt', '')  # Extraer nombre sin extensión

        # Leer el contenido del archivo de texto
        document_text = read_text_from_file(document_location)

        # Imprimir el texto completo para ver su estructura
        print(f"Contenido del archivo {file_name}:")
        print(document_text[:500])  # Imprime los primeros 500 caracteres para depuración
        print("="*50)

        # Crear un diccionario para cada entrada
        document_dict = {
            "computerbot": file_name,
            "marca": [],
            "modelo": [],
            "sistema operativo": [],
            "procesador": [],
            "memoria ram": [],
            "almacenamiento": [],
            "tarjeta grafica": [],
            "peso": [],
            "duracion": [],
            "codigo": [],
            "precio": [],
            "garantia": [],
            "disco duro": [],
            "memoria grafica": [],
            "modelo grafica": [],
            "frecuencia procesador": [],
            "pantalla": [],
            "resolucion": [],
            "altura": [],
            "ancho": [],
            "color": [],
            "bluetooth": [],
            "usabilidad": [],
            "equipo": [],
            "puerto USB": [],
            "garantia modelo": [],
            "material": []
        }

        # Extraer las entidades del documento
        for entity in document['entities']:
            for label in entity['labels']:
                category = label['category']
                # Asegúrate de que la categoría esté en el diccionario
                if category in document_dict:
                    # Extraer el texto correspondiente a esa entidad usando el offset y length
                    entity_text = document_text[label['offset']:label['offset'] + label['length']]

                    # Imprimir la entidad extraída para depuración
                    print(f"Categoría: {category}")
                    print(f"Texto extraído: '{entity_text}'")
                    print("="*50)

                    # Añadir el texto extraído a la lista de esa categoría
                    document_dict[category].append(entity_text)

        # Guardar el resultado en un archivo JSON
        output_filename = f"{output_directory}/{file_name}.json"
        os.makedirs(output_directory, exist_ok=True)  # Crear la carpeta de salida si no existe
        with open(output_filename, 'w', encoding='utf-8') as json_file:
            json.dump(document_dict, json_file, ensure_ascii=False, indent=4)

        print(f"Item insertado: {file_name}")

# Procesar los datos
process_ner_data(ner_data)
