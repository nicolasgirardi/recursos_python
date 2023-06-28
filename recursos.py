from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import psycopg2
from psycopg2 import Error
from flask_swagger import swagger


app = Flask(__name__)
CORS(app)
import urllib.parse
db_url = "postgres://squad5_tribu_d_user:01miMzjN49jnnBf3r2utmwF5IxOMyKtT@dpg-ci5p8mdph6eh6mq9qsv0-a.oregon-postgres.render.com/squad5_tribu_d"
parsed_url = urllib.parse.urlparse(db_url)
hostrender = parsed_url.hostname
try:
    connection = psycopg2.connect(
        host=hostrender,
        port="5432",
        dbname="squad5_tribu_d",
        user="squad5_tribu_d_user",
        password="01miMzjN49jnnBf3r2utmwF5IxOMyKtT"
    )
    print("Conexión exitosa a PostgreSQL en Render")
except (Exception, psycopg2.Error) as error:
    print("Error durante la conexión a PostgreSQL en Render:", error)

# Mock RecursoService y CargaHorasService para simplificar el ejemplo
class RecursoService:
    def findAllLegajos(self):
        # Implementación de ejemplo para devolver un Recurso
        url = 'https://anypoint.mulesoft.com/mocking/api/v1/sources/exchange/assets/754f50e8-20d8-4223-bbdc-56d50131d0ae/recursos-psa/1.0.1/m/api/recursos'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data
        else: 
            return None
    def findByLegajo(self,legajo_buscado):
        url = 'https://anypoint.mulesoft.com/mocking/api/v1/sources/exchange/assets/754f50e8-20d8-4223-bbdc-56d50131d0ae/recursos-psa/1.0.1/m/api/recursos'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            for elemento in data:
                if elemento['legajo'] == legajo_buscado:
                    return elemento
                    break
        else: 
            return None

class CargaHorasService:
    def cargarHoras(self, legajo, tarea, cantidadHoras, fecha):
        # Implementación de ejemplo para simular carga exitosa o fallida
        if legajo == 123:
            return True
        else:
            return False

recursoService = RecursoService()
cargaHorasService = CargaHorasService()

@app.route('/recursos',methods=['GET'])
def getLegajo():
    legajo = request.args.get('legajo')
    recurso = recursoService.findByLegajo(legajo)
    if recurso is None:
        return jsonify(error="Recurso no encontrado"), 404
    return jsonify(recurso)

@app.route('/recurso',methods=['GET'])
def getLegajos():
    recurso = recursoService.findAllLegajos()
    if recurso is None:
        return jsonify(error="Recurso no encontrado"), 404
    return jsonify(recurso)

@app.route('/cargaHoras', methods=['POST'])
def cargarHoras():
    legajo = request.form.get('legajo')
    tarea = request.form.get('tarea')
    cantidadHoras = request.form.get('cantidadHoras')
    fecha = request.form.get('fecha')
    cargaExitosa = cargaHorasService.cargarHoras(legajo, tarea, cantidadHoras, fecha)
    if cargaExitosa:
        return "Carga de horas exitosa"
    else:
        return jsonify(error="No se pudo cargar las horas"), 500
    
@app.route('/')
def index():
    return "¡Hola, mundo!"

@app.route('/swagger')
def swagger_spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "API de ejemplo"
    return jsonify(swag)

if __name__ == '__main__':
    app.run(port=8080)