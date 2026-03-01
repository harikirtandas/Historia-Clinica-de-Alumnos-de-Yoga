from app import db
from datetime import date

class Alumno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    edad = db.Column(db.Integer)
    signo_zodiaco = db.Column(db.String(30))
    profesion = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120))
    fecha_alta = db.Column(db.Date, default=date.today)

    fuma = db.Column(db.Boolean, default=False)
    patologias_fisicas = db.Column(db.Text)
    patologias_psicologicas = db.Column(db.Text)
    toma_medicacion = db.Column(db.Boolean, default=False)
    medicacion = db.Column(db.Text)
    presion_sanguinea = db.Column(db.String(20))
    practica_yoga_previamente = db.Column(db.Boolean, default=False)
    motivo_practica = db.Column(db.Text)
    realiza_actividad_fisica = db.Column(db.Boolean, default=False)
    como_nos_conocio = db.Column(db.String(200))
    observaciones_generales = db.Column(db.Text)

    def edad_calculada(self):
        if not self.fecha_nacimiento:
            return None
        hoy = date.today()
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )
