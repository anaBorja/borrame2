import os
from dotenv import load_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Cargar las variables del archivo .env
load_dotenv()

# Leer las credenciales desde las variables de entorno
endpoint = os.getenv("FORM_RECOGNIZER_ENDPOINT")
key = os.getenv("FORM_RECOGNIZER_KEY")

# Inicializar el cliente de Form Recognizer
client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Función para convertir PDF a texto

def convert_pdf_to_text(pdf_path):
    with open(pdf_path, "rb") as f:
        # Usar el modelo 'prebuilt-layout' en lugar de 'prebuilt-document'
        poller = client.begin_analyze_document("prebuilt-layout", document=f)
        result = poller.result()

        extracted_text = result.content
        return extracted_text

# Función para procesar todos los PDFs en una carpeta y guardar los .txt en otra carpeta
def process_pdfs_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            print(f"Procesando: {filename}")

            text = convert_pdf_to_text(pdf_path)
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            txt_path = os.path.join(output_folder, txt_filename)

            with open(txt_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(text)
            print(f"Texto guardado en: {txt_path}")

# Definir las carpetas de entrada y salida
input_folder = os.path.join(os.getcwd(), "Fichas técnicas")
output_folder = os.path.join(os.getcwd(), "text_output")

# Procesar los PDFs
process_pdfs_in_folder(input_folder, output_folder)
