import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db
from models import User, Job

def create_app():
    app = Flask(__name__)

    # Base de datos: usa DATABASE_URL si existe (Render Postgres), si no, SQLite local
    db_url = os.environ.get("DATABASE_URL", "sqlite:///jobs.db")
    # Render a veces da un URL "postgres://" -> SQLAlchemy prefiere "postgresql://"
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    CORS(app)

    # Crear tablas en el arranque
    with app.app_context():
        db.create_all()

    # ---------- Rutas ----------
    @app.route("/", methods=["GET"])
    def root():
        return jsonify({"status": "ok", "service": "app-discrear"})

    @app.route("/register", methods=["POST"])
    def register():
        data = request.get_json(force=True)
        name = data.get("name")
        role = data.get("role")
        if not name or role not in ("worker", "employer"):
            return jsonify({"error": "Datos inválidos. role debe ser 'worker' o 'employer'."}), 400
        user = User(name=name, role=role)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuario registrado", "user_id": user.id}), 201

    @app.route("/jobs", methods=["POST"])
    def create_job():
        data = request.get_json(force=True)
        employer_id = data.get("employer_id")
        title       = data.get("title")
        description = data.get("description")
        date        = data.get("date")
        location    = data.get("location")
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
        return jsonify({"message": "Trabajo publicado", "job_id": job.id}), 201

    @app.route("/jobs", methods=["GET"])
    def list_jobs():
        # filtros opcionales ?date=YYYY-MM-DD&location=Bogota&title=montaje
        date_q     = request.args.get("date")
        location_q = request.args.get("location")
        title_q    = request.args.get("title")

        query = Job.query
        if date_q:
            query = query.filter(Job.date == date_q)
        if location_q:
            query = query.filter(Job.location.ilike(f"%{location_q}%"))
        if title_q:
            query = query.filter(Job.title.ilike(f"%{title_q}%"))

        jobs = query.all()
        return jsonify([
            {
                "id": j.id, "title": j.title, "description": j.description,
                "date": j.date, "location": j.location, "employer_id": j.employer_id
            } for j in jobs
        ])

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
