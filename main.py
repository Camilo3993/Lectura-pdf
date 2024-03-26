# Importar la clase Flask del módulo flask
from flask import Flask
# Importar la clase Api del módulo flask_smorest
from flask_smorest import Api

# Importar los blueprints (conjuntos de rutas) definidos en otros archivos
# blp: Blueprint
from resources.link import blp as LinkBlueprint

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Configurar la aplicación Flask
# Habilitar la propagación de excepciones, lo que permite que las excepciones
# en las vistas sean propagadas para que Flask las maneje
app.config["PROPAGATE_EXCEPTIONS"] = True
# Configurar el título de la API
app.config["API_TITLE"] = "Epysa API"
# Configurar la versión de la API
app.config["API_VERSION"] = "v1"
# Configurar la versión de OpenAPI
app.config["OPENAPI_VERSION"] = "3.0.3"
# Configurar el prefijo de la URL de OpenAPI
app.config["OPENAPI_URL_PREFIX"] = "/"
# Configurar la ruta de la interfaz de usuario de Swagger UI
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
# Configurar la URL de la interfaz de usuario de Swagger UI
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Crear una instancia de la clase Api y asociarla con la aplicación Flask
api = Api(app)

# Registrar los blueprints en la instancia de la clase Api
api.register_blueprint(LinkBlueprint)  # Registrar el blueprint para las preguntas


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug = True)