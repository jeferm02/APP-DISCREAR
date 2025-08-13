from flask import Flask, jsonify

app = Flask(__name__)

# Ruta raíz para probar que el servidor funciona
@app.route("/")
def home():
    return jsonify({"mensaje": "Servidor Flask funcionando en Render"})

# Ejemplo de otra ruta de API
@app.route("/api/saludo", methods=["GET"])
def saludo():
    return jsonify({"saludo": "Hola desde Flask en Render"})

if __name__ == "__main__":
    # Render necesita escuchar en 0.0.0.0 y usar el puerto que indique la variable PORT
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

