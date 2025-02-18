import os
import re

# Definir la función extract_info
def extract_info(text, patterns):
    extracted_data = {}
    for key, pattern in patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        extracted_data[key] = [match[0] if isinstance(match, tuple) else match for match in matches] if matches else None
    return extracted_data


# Definir las rutas relativas usando os.path.join
current_dir = os.path.dirname(__file__)  # Obtiene el directorio donde se encuentra el script
input_folder = os.path.join(current_dir, 'text_output')  # Carpeta con los archivos .txt de entrada
output_folder = os.path.join(current_dir, 'cleaned_txt')  # Carpeta donde se guardarán los archivos procesados

# Asegurarse de que la carpeta de salida exista
os.makedirs(output_folder, exist_ok=True)

# Función para limpiar y extraer las especificaciones del texto
def extract_specs_and_clean(text):
    # Limpiar datos no disponibles
    not_available_pattern = r'(No disponible|N/A|sin datos|sin información)'
    cleaned_text = re.sub(not_available_pattern, '', text)

     # Diccionario para las especificaciones
    specs = {
        'Garantía': None,
        'Disco Duro': None,
        'Tipo Soporte Disco': None,
        'Interfaz Soporte': None,
        'Número Soportes': None,
        'Gráfica': None,
        'Fabricante Gráfica': None,
        'Modelo':None,
        'Modelo Gráfica': None,
        'Memoria Gráfica': None,
        'Familia Procesador': None,
        'Modelo Procesador': None,
        'Fabricante Procesador': None,
        'Frecuencia Procesador': None,
        'Pantalla': None,
        'Precio': None,
        'Tamaño Pantalla': None,
        'Pantalla Táctil': None,
        'Tipo Pantalla': None,
        'Resolución Pantalla': None,
        'Superficie Pantalla': None,
        'Peso': None,
        'Altura': None,
        'Ancho': None,
        'Profundidad': None,
        'Color': None,
        'Trusted Platform Module (TPM)': None,
        'Conexión a Red Móvil': None,
        'Puertos USB': None,
        'Ethernet': None,
        'Bluetooth': None,
        'Puerto Thunderbolt': None,
        'Puerto HDMI': None,
        'RAM': None,
        'RAM Instalada': None,
        'RAM Máxima': None,
        'Bancos RAM Libres': None,
        'Velocidad RAM': None,
        'Tecnología RAM': None,
        'Unidad Óptica': None,
        'Teclado': None,
        'Micrófono Integrado': None,
        'Número de Celdas Batería': None,
        'Duración de la Batería': None,
        'Webcam': None,
        'Resolución Webcam': None,
        'Sistema Operativo': None,
        'Pluma': None,
        'Opciones': None,
        'Otros': []
    }

    # Expresiones regulares ajustadas para manejar las variaciones
    patterns = {
        'Garantía': r'Garantía\s?:?\s?(\d+\s?(años|meses))',
        'Disco Duro': r'Disco\s?duro\s?:?\s?(\d+(?:\.\d+)?\s?(GB|TB))',
        'Tipo Soporte Disco': r'Tipo\s?Soporte\s?1\s?:?\s?(HDD|SSD|NVMe|eMMC|SATA|PCIe)',
        'Interfaz Soporte': r'Interfaz\s?Soporte\s?1\s?:?\s?(SATA\s?\d+|PCIe\s?\d+|NVMe|eMMC)',
        'Número Soportes': r'Número\s?Soportes\s?:?\s?(\d+)',
        'Gráfica': r'(NVIDIA\s?(GeForce|Quadro|RTX|GTX|Tesla|Titan)\s?\d*\w*|AMD\s?(Radeon|RX|Pro|FirePro)\s?\d*\w*|Intel\s?(Iris|UHD|HD\s?Graphics|Arc))',
        'Fabricante Gráfica': r'Fabricante\s?de\s?la\s?gráfica\s?:?\s?(NVIDIA|AMD|Intel)',
        'Modelo': r'(?i)(Galaxy Book\d* Ultra|MacBook Pro|MacBook Air|ThinkPad X\d+|ThinkPad T\d+|Inspiron \d+|XPS \d+|ROG Zephyrus|ROG Strix|Predator Helios|Acer Swift|Surface Laptop \d+|Surface Pro \d+)',
        'Modelo Gráfica': r'Modelo\s?gráfica\s?:?\s?([\w\s-]+)',
        'Memoria Gráfica': r'Memoria\s?de\s?la\s?gráfica\s?:?\s?(\d+\s?(MB|GB))',
        'Familia Procesador': r'Familia\s?Procesador\s?:?\s?(Intel\s?Core|AMD\s?Ryzen|Apple\s?M\d+|Intel\s?Xeon|AMD\s?EPYC)',
        'Modelo Procesador': r'(Intel\s?Core\s?(i\d+|Ultra)|AMD\s?Ryzen\s?\d+\s?\d+\w*|Apple\s?M\d+|Intel\s?Xeon\s?\w+|AMD\s?EPYC\s?\w+)',
        'Fabricante Procesador': r'Fabricante\s?procesador\s?:?\s?(Intel|AMD|Apple)',
        'Frecuencia Procesador': r'(?i)Frecuencia\s?del\s?procesador\s?:?\s?(\d+\.\d+\s?GHz|\d+(\.\d+)?\s?GHz)',
        'Pantalla': r'(\d{2}(\.\d{1,2})?\s*(pulgadas|"))',
        'Precio': r'(\d+\.\d+,\d{2}\s?€|\d+\s?€)',
        'Tamaño Pantalla': r'(\d+(\.\d+)?\s?(pulgadas|"))',
        'Pantalla Táctil': r'Pantalla\s?táctil\s?:?\s?(Sí|No)',
        'Tipo Pantalla': r'Tipo\s?de\s?pantalla\s?:?\s?(IPS|OLED|AMOLED|TN|VA|LCD)',
        'Resolución Pantalla': r'Resolución\s?:?\s?(\d{3,4}\s?×\s?\d{3,4})',
        'Superficie Pantalla': r'Superficie\s?de\s?la\s?pantalla\s?:?\s?(Mate|Brillante)',
        'Peso': r'(\d+(\.\d+)?\s*(kg|g))',
        'Tamaño': r'(\d+(\.\d+)?\s*x\s*\d+(\.\d+)?\s*x\s*\d+(\.\d+)?\s*(cm|mm|m))',
        'Altura': r'(\d+(\.\d+)?\s*(mm|cm|m))(?=\s*(Altura))',
        'Ancho': r'(\d+(\.\d+)?\s*(mm|cm|m))(?=\s*(Ancho))',
        'Profundidad': r'(\d+(\.\d+)?\s*(mm|cm|m))(?=\s*(Profundidad))',
        'Color': r'(Negro|Blanco|Gris|Plateado|Plata|Dorado|Oro|Azul|Rojo|Verde|Amarillo|Naranja|Rosa|Morado|Violeta|Cian|Turquesa|Marrón|Beige|Crema|Grafito|Antracita|Fucsia|Celeste|Coral|Burdeos|Granate|Lima|Caqui|Mostaza|Lavanda|Oliva|Índigo|Perla|Chocolate|Marfil|Esmeralda|Carbón|Champán|Cobre|Titanio)(\s?(Mate|Brillante|Metálico|Oscuro|Claro|Satinado))?',
        'Trusted Platform Module (TPM)': r'Trusted\s?Platform\s?Module\s?:?\s?(Sí|No)',
        'Conexión a Red Móvil': r'Conexión\s?a\s?red\s?móvil\s?:?\s?(5G|4G|LTE|No)',
        'Puertos': r'(USB\s?(2\.0|3\.0|3\.1|3\.2|4|Tipo-C)|Thunderbolt\s?(3|4)|HDMI\s?(1\.4|2\.0|2\.1)|Ethernet\s?(10/100|Gigabit|2\.5G|10G)|DisplayPort\s?(1\.2|1\.4|2\.0)|VGA|DVI|Jack\s?(3\.5mm|audio)|SD\s?Card\s?Reader)',
        'Ethernet': r'Ethernet\s?:?\s?(Sí|No|Gigabit|10/100/1000)',
        'Bluetooth': r'Bluetooth\s?:?\s?(5\.\d+|4\.\d+|No)',
        'Puerto Thunderbolt': r'Puerto\s?Thunderbolt\s?:?\s?(3|4|No)',
        'Puerto HDMI': r'Puerto\s?HDMI\s?:?\s?(1\.\d|2\.\d|No)',
        'RAM': r'RAM\s?:?\s?(\d+\s?GB)',
        'RAM Instalada':  r'(\d+\s*GB)(?=\s*(RAM Instalada))',
        'RAM Máxima': r'(\d+\s*GB)(?=\s*(RAM Máxima))',
        'Bancos RAM Libres': r'(\d+)(?=\s*(Bancos RAM Libres))',
        'Velocidad RAM':r'(\d+\s*MHz)',
        'Tecnología RAM': r'(DDR[1-5]|LPDDR[1-5]|DDR3|DDR4|DDR5|LPDDR4X|LPDDR5X)',
        'Unidad Óptica': r'Unidad\s?Óptica\s?:?\s?(DVD|Blu-ray|No)',
        'Teclado': r'Teclado\s?:?\s?(Retroiluminado|Mecánico|Membrana|No)',
        'Micrófono Integrado': r'Micrófono\s?Integrado\s?:?\s?(Sí|No)',
        'Número de Celdas Batería': r'Número\s?celulas\s?de\s?la\s?batería\s?:?\s?(\d+)',
        'Duración de la Batería': r'Duración\s?de\s?la\s?batería\s?:?\s?(\d+\s?h)',
        'Webcam': r'Webcam\s?:?\s?(Sí|No|HD|Full HD|4K)',
        'Resolución Webcam': r'Resolución\s?de\s?la\s?Webcam\s?:?\s?(\d+\s?p)',
        'Sistema Operativo': r'(Windows\s?(XP|Vista|7|8|10|11|Home|Pro|Enterprise|Education|S|RT|Mobile)?)',
        'Pluma': r'Pluma\s?:?\s?(Sí|No)',
        'Opciones': r'Opciones\s?:?\s?([\w\s,]+)',
        'Otros': r'Otros\s?:?\s?([\w\s,]+)'
    }

    # Buscar patrones en el texto
    for key, pattern in patterns.items():
        match = re.search(pattern, cleaned_text, re.IGNORECASE)  # Agregar re.IGNORECASE para que sea insensible a mayúsculas
        if match:
            specs[key] = match.group(1)

    return specs

# Leer todos los archivos .txt en la carpeta de entrada
for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        file_path = os.path.join(input_folder, filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Extraer especificaciones y limpiar el contenido
        specs = extract_specs_and_clean(text)

        # Ordenar las claves de las especificaciones antes de escribirlas
        sorted_specs = specs

        # Crear el archivo de salida con el nombre procesado
        output_file_path = os.path.join(output_folder, f"cleaned_{filename}")
        
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for spec, value in sorted_specs.items():
                if value:
                    output_file.write(f"{spec}: {value}\n")
                else:
                    output_file.write(f"{spec}: No disponible\n")

print("Proceso completado.")
