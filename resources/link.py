import os
import tempfile
from schemas import LinkSchema
from flask.views import MethodView
from flask_smorest import Blueprint
import pdfplumber
from flask import Flask, request, jsonify
import requests

# Crea un objeto Blueprint llamado "link" con descripción "enviar link y extraer la informacion del documento"
blp = Blueprint("link", "links", description="enviar link y extraer la informacion del documento")

# Define una ruta "/link" dentro del Blueprint
@blp.route("/link")
# Define una clase llamada Link que hereda de MethodView
class Link(MethodView):
    # Define un método POST para enviar un link
    @blp.arguments(LinkSchema)
    # Código 201 que indica que se creó un nuevo link 
    @blp.response(201, LinkSchema)
    # Define la función post que toma el link como parámetro
    def post(self, link):
        # Extrae el JSON del request
        json_data = request.json

        # Verifica si el JSON es válido y contiene el campo "link"
        if not json_data or 'link' not in json_data:
            return jsonify({"error": "Formato JSON inválido"}), 400  

        # Obtiene el link y el nombre del JSON
        link = json_data.get('link')
        nombre = json_data.get('nombre')

        # Realiza una solicitud GET al enlace para verificar si es válido y se puede descargar el PDF
        response = requests.get(link)

        # Verifica si la solicitud fue exitosa (código de estado 200)
        if response.status_code != 200 or response.headers.get('content-type') != 'application/pdf':
            return jsonify({"error": "El enlace proporcionado no es válido o no se puede descargar el PDF"}), 400

        # Obtener el sistema operativo
        sistema_operativo = os.name  # 'posix' para Unix/Linux/MacOS, 'nt' para Windows

        # Crear un directorio temporal usando la ruta apropiada para el sistema operativo
        directorio_temporal = None
        if sistema_operativo == 'posix':  # Unix/Linux/MacOS
            directorio_temporal = tempfile.mkdtemp()
        elif sistema_operativo == 'nt':  # Windows
            directorio_temporal = tempfile.mkdtemp()
        else:
            return jsonify({"error": "Sistema operativo no compatible"}), 400

        # Construir la ruta del archivo PDF en el directorio temporal
        ruta_pdf = os.path.join(directorio_temporal, f"{nombre}.pdf")

        # Guardar el archivo PDF en la ruta construida
        with open(ruta_pdf, "wb") as pdf_file:
            pdf_file.write(response.content)

        print("Archivo PDF descargado correctamente en la ruta:", ruta_pdf)

        # Define una lista para almacenar las tablas extraídas
        tablas_extraidas = []

        # Abre el archivo PDF con pdfplumber
        with pdfplumber.open(ruta_pdf) as pdf:
            for num_pagina, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "lines"})

                if not tables:
                    continue

                num_tabla_pagina = 1  # Inicializa el contador de tablas por página
                for table in tables:
                    tabla_dict = {
                        "numero_pagina": num_pagina,
                        "numero_tabla": num_tabla_pagina,
                        "contenido": table
                    }
                    tablas_extraidas.append(tabla_dict)
                    
                    num_tabla_pagina += 1

        # Agrega las tablas extraídas a los datos de respuesta
        response_data = {'test': link, 'nombre': nombre, 'pdf': tablas_extraidas}

        # Retorna los datos de respuesta en formato JSON
        return jsonify(response_data)

