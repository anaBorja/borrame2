import json
import os

# Ruta del archivo JSON sin formato
input_folder = "contenedordpf/"  # Cambia esto según la ubicación del archivo de entrada

# Carpeta donde se guardarán los archivos formateados
output_folder = "formateado"

# Asegurarse de que la carpeta de salida exista
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


# Recorrer todos los archivos en la carpeta de entrada
for filename in os.listdir(input_folder):
    # Verificar si el archivo es un .json
    if filename.endswith(".json") and filename.endswith(".labels.json"):
        input_file_path = os.path.join(input_folder, filename)

        # Leer el archivo JSON sin formato
        with open(input_file_path, 'r') as file:
            try:
                data = json.load(file)

                # Ruta del archivo de salida con el formato adecuado
                output_file_path = os.path.join(output_folder, filename)

                # Guardar el archivo con formato
                with open(output_file_path, 'w') as outfile:
                    json.dump(data, outfile, indent=4)  # Usar indentación de 4 espacios

                print(f"Archivo procesado y guardado: {output_file_path}")
            except json.JSONDecodeError:
                print(f"Error al procesar el archivo: {filename}")




















"""
# Leer el archivo sin formato
with open(input_file_path, 'r') as file:
    data = json.load(file)

# Ruta del archivo de salida con el formato adecuado
output_file_path = os.path.join(output_folder, os.path.basename(input_file_path))

# Guardar el archivo con formato
with open(output_file_path, 'w') as file:
    json.dump(data, file, indent=4)  # Usar indentación de 4 espacios

print(f"El archivo formateado se ha guardado en: {output_file_path}")
"""