from database import db

class User(db.Model):
    __tablename__ = "users"
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20),  nullable=False)  # "worker" o "employer"

class Job(db.Model):
    __tablename__ = "jobs"
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date        = db.Column(db.String(20))        # simplificado (YYYY-MM-DD)
    location    = db.Column(db.String(120))
    employer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
