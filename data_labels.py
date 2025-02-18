import os
import json

# Función para extraer el texto de una etiqueta
def extraer_texto_label(labels, label_name):
    for label in labels:
        if label['label'].lower() == label_name.lower():
            # Obtener el texto de la etiqueta (asumiendo que siempre hay solo un valor por etiqueta)
            return label['value'][0]['text']
    return None  # Si no se encuentra la etiqueta, devolver None

# Ruta de la carpeta de entrada y salida
input_folder = "formateado"  # Carpeta con los archivos JSON originales
output_folder = "json_folder"  # Carpeta donde se guardarán los archivos formateados

# Crear la carpeta de salida si no existe
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Función para procesar todos los archivos JSON en la carpeta de entrada
def procesar_archivos(input_folder, output_folder):
    # Recorrer todos los archivos en la carpeta de entrada
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            input_file_path = os.path.join(input_folder, filename)
            
            # Leer el archivo JSON
            with open(input_file_path, 'r') as file:
                data = json.load(file)
            
            # Extraer las etiquetas
            labels = data.get('labels', [])
            
            # Crear el nuevo formato de JSON
            output_data = {
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
                "codigo": "codigo_example",  # Este es un ejemplo, se puede modificar según sea necesario
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
            
            # Guardar el nuevo archivo JSON en la carpeta de salida
            output_file_path = os.path.join(output_folder, filename)
            with open(output_file_path, 'w') as outfile:
                json.dump(output_data, outfile, indent=4)
            
            print(f"Archivo procesado y guardado en: {output_file_path}")

# Llamar a la función para procesar los archivos
procesar_archivos(input_folder, output_folder)
