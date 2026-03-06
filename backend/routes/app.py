from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from routes.auth import auth_bp
from routes.usuarios import usuarios_bp
from routes.lotes import lotes_bp
from routes.compras import compras_bp
from routes.pagos import pagos_bp
from routes.pqrs import pqrs_bp
from routes.etapas import etapas_bp
from routes.proyecto import proyecto_bp

app = Flask(_name_)
CORS(app)

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')
app.register_blueprint(lotes_bp, url_prefix='/api/lotes')
app.register_blueprint(compras_bp, url_prefix='/api/compras')
app.register_blueprint(pagos_bp, url_prefix='/api/pagos')
app.register_blueprint(pqrs_bp, url_prefix='/api/pqrs')
app.register_blueprint(etapas_bp, url_prefix='/api/etapas')
app.register_blueprint(proyecto_bp, url_prefix='/api/proyecto')

@app.route('/')
def index():
    return {'message': 'API Inmobiliario funcionando ✅', 'version': '1.0'}

if _name_ == '_main_':
    app.run(debug=True, port=5000)