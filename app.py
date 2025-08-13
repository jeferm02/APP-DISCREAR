from flask import Flask, request, jsonify
from models import User, Job
from database import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jobs.db"
db.init_app(app)

# Crear las tablas al iniciar la aplicación
with app.app_context():
    db.create_all()

# Ruta para registrar usuarios (empresa o trabajador)
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    role = data.get("role")

    if not name or not role:
        return jsonify({"error": "Faltan datos"}), 400

    user = User(name=name, role=role)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Usuario registrado", "user_id": user.id})

# Ruta para publicar trabajos (solo empresas)
@app.route("/jobs", methods=["POST"])
def create_job():
    data = request.get_json()
    employer_id = data.get("employer_id")
    title = data.get("title")
    description = data.get("description")
    date = data.get("date")
    location = data.get("location")

    if not all([employer_id, title, description]):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    job = Job(
        employer_id=employer_id,
        title=title,
        description=description,
        date=date,
        location=location
    )
    db.session.add(job)
    db.session.commit()
    return jsonify({"message": "Trabajo publicado", "job_id": job.id})

# Ruta para listar todos los trabajos publicados
@app.route("/jobs", methods=["GET"])
def list_jobs():
    jobs = Job.query.all()
    results = [
        {
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "date": job.date,
            "location": job.location,
            "employer_id": job.employer_id
        }
        for job in jobs
    ]
    return jsonify(results)

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
