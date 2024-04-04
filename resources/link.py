import os
import tempfile

# Importa la clase MethodView de flask.views
from flask.views import MethodView
# Importa la clase Blueprint y la función abort de flask_smorest
from flask_smorest import Blueprint, abort

import pdfplumber

# Importa el esquema PreguntaSchema desde el archivo schemas.py
from schemas import LinkSchema
from flask import Flask, request, jsonify ,session
import requests

from bs4 import BeautifulSoup

# Crea un objeto Blueprint llamado "pregunta" con descripción "enviar pregunta y obtener respuesta"
blp = Blueprint("link", "links", description="enviar link y extraer la informacion del documento")



# Define una ruta "/pregunta" dentro del Blueprint
@blp.route("/link")
# Define una clase llamada pregunta que hereda de MethodView
class Link(MethodView):
    # Define un método POST para enviar una pregunta
    @blp.arguments(LinkSchema)
    # codigo 201 que indica que se creo una nueva pregunta 
    @blp.response(201, LinkSchema)
    # Define la función post que toma pregunta como parámetro
    def post(self, link):
        

        json_data = request.json
        

        if not json_data or 'link' not in json_data:
            return jsonify({"error": "Invalid JSON format"}), 400  

        link = json_data.get('link')
        nombre = json_data.get('nombre')
        response = requests.get(link)


        # Obtener el sistema operativo
        sistema_operativo = os.name  # 'posix' para Unix/Linux/MacOS, 'nt' para Windows

        # Crear un directorio temporal para descargar el PDF
        directorio_temporal = tempfile.mkdtemp()

        # Luego, puedes usar este directorio temporal para guardar el archivo PDF
        ruta_pdf = os.path.join(directorio_temporal, f"{nombre}.pdf")

        # Guardar el archivo PDF en el directorio temporal
        with open(ruta_pdf, "wb") as pdf_file:
            pdf_file.write(response.content)

        print("Archivo PDF descargado correctamente en el directorio temporal:", ruta_pdf)



        # Define una lista para almacenar las tablas extraídas
        tablas_extraidas = []

        # Abre el archivo PDF con pdfplumber
        with pdfplumber.open(ruta_pdf) as pdf:
            # Itera sobre todas las páginas del PDF
            for num_pagina, page in enumerate(pdf.pages, start=1):
                # Extrae las tablas de la página actual
                tables = page.extract_tables(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "lines"})

                # Si no hay tablas en esta página, pasa a la siguiente
                if not tables:
                    continue

                # Enumera las tablas en la página actual
                for num_tabla, table in enumerate(tables, start=1):
                    # Organiza los datos de la tabla para agrupar los valores de cada columna
                    tabla_procesada = []
                    num_columnas = len(table[0])  # Obtén el número de columnas de la tabla
                    for i in range(num_columnas):
                        columna = [fila[i] for fila in table if fila[i] is not None]  # Extrae los valores de la columna
                        tabla_procesada.append(columna)

                    # Agrega la información de la tabla procesada a la lista de tablas extraídas
                    tablas_extraidas.append({
                        "numero_pagina": num_pagina,
                        "numero_tabla": num_tabla,
                        "contenido": tabla_procesada
                    })

        # Agrega las tablas extraídas a los datos de respuesta
        response_data = {'test': link, 'nombre': nombre, 'tablas': tablas_extraidas}

        # Retorna los datos de respuesta en formato JSON
        return jsonify(response_data)