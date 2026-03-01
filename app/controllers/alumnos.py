from datetime import date, datetime
import textwrap

from flask import Blueprint, redirect, render_template, request, url_for
from sqlalchemy import or_

from app import db
from app.models.alumno import Alumno

alumnos_bp = Blueprint("alumnos", __name__)


def _parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def _bool_from_form(value):
    return value == "on"


def _parse_int(value):
    if value is None:
        return None
    value = str(value).strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _zodiac_from_date(fecha):
    if not fecha:
        return None
    month = fecha.month
    day = fecha.day
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    if (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Tauro"
    if (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Geminis"
    if (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    if (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    if (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    if (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    if (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Escorpio"
    if (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagitario"
    if (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricornio"
    if (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Acuario"
    return "Piscis"


def _age_from_date(fecha):
    if not fecha:
        return None
    today = date.today()
    years = today.year - fecha.year
    if (today.month, today.day) < (fecha.month, fecha.day):
        years -= 1
    return years


def _required_fields_missing(nombre, apellido, telefono):
    missing = []
    if not nombre:
        missing.append("nombre")
    if not apellido:
        missing.append("apellido")
    if not telefono:
        missing.append("telefono")
    return missing


def _form_data_from_request():
    return {
        "nombre": request.form.get("nombre", "").strip(),
        "apellido": request.form.get("apellido", "").strip(),
        "fecha_nacimiento": request.form.get("fecha_nacimiento", ""),
        "edad": request.form.get("edad", "").strip(),
        "signo_zodiaco": request.form.get("signo_zodiaco", "").strip(),
        "profesion": request.form.get("profesion", ""),
        "telefono": request.form.get("telefono", "").strip(),
        "email": request.form.get("email", ""),
        "fuma": _bool_from_form(request.form.get("fuma")),
        "patologias_fisicas": request.form.get("patologias_fisicas", ""),
        "patologias_psicologicas": request.form.get("patologias_psicologicas", ""),
        "toma_medicacion": _bool_from_form(request.form.get("toma_medicacion")),
        "medicacion": request.form.get("medicacion", ""),
        "presion_sanguinea": request.form.get("presion_sanguinea", ""),
        "practica_yoga_previamente": _bool_from_form(
            request.form.get("practica_yoga_previamente")
        ),
        "motivo_practica": request.form.get("motivo_practica", ""),
        "realiza_actividad_fisica": _bool_from_form(
            request.form.get("realiza_actividad_fisica")
        ),
        "como_nos_conocio": request.form.get("como_nos_conocio", ""),
        "observaciones_generales": request.form.get("observaciones_generales", ""),
    }


def _form_data_from_model(alumno):
    return {
        "nombre": alumno.nombre or "",
        "apellido": alumno.apellido or "",
        "fecha_nacimiento": alumno.fecha_nacimiento.isoformat()
        if alumno.fecha_nacimiento
        else "",
        "edad": str(alumno.edad) if alumno.edad is not None else "",
        "signo_zodiaco": alumno.signo_zodiaco or "",
        "profesion": alumno.profesion or "",
        "telefono": alumno.telefono or "",
        "email": alumno.email or "",
        "fuma": bool(alumno.fuma),
        "patologias_fisicas": alumno.patologias_fisicas or "",
        "patologias_psicologicas": alumno.patologias_psicologicas or "",
        "toma_medicacion": bool(alumno.toma_medicacion),
        "medicacion": alumno.medicacion or "",
        "presion_sanguinea": alumno.presion_sanguinea or "",
        "practica_yoga_previamente": bool(alumno.practica_yoga_previamente),
        "motivo_practica": alumno.motivo_practica or "",
        "realiza_actividad_fisica": bool(alumno.realiza_actividad_fisica),
        "como_nos_conocio": alumno.como_nos_conocio or "",
        "observaciones_generales": alumno.observaciones_generales or "",
    }


def _safe_text(value, width=60):
    if value is None:
        return "-"
    text = str(value).replace("\r\n", "\n").replace("\r", "\n")
    lines = []
    for line in text.split("\n"):
        if not line.strip():
            lines.append("")
            continue
        lines.append(textwrap.fill(line, width=width, break_long_words=True))
    return "\n".join(lines)


def _break_long_words(text, max_len=60):
    words = []
    for word in text.split(" "):
        if len(word) <= max_len:
            words.append(word)
            continue
        chunks = [word[i : i + max_len] for i in range(0, len(word), max_len)]
        words.append(" ".join(chunks))
    return " ".join(words)


def _pdf_multiline(pdf, text, line_height=6):
    pdf.set_x(pdf.l_margin)
    width = pdf.w - pdf.l_margin - pdf.r_margin
    safe = _break_long_words(_safe_text(text), max_len=60)
    pdf.multi_cell(width, line_height, safe, align="L")


def _pdf_bytes(pdf):
    output = pdf.output(dest="S")
    if isinstance(output, str):
        return output.encode("latin1")
    return bytes(output)


def _new_pdf():
    # Import diferido: si falla la dependencia de PDF, la app puede iniciar igual.
    from fpdf import FPDF

    return FPDF()

@alumnos_bp.route("/")
def home():
    return redirect(url_for("alumnos.listar"))


@alumnos_bp.route("/alumnos")
def listar():
    q = request.args.get("q", "").strip()
    query = Alumno.query
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Alumno.nombre.ilike(like),
                Alumno.apellido.ilike(like),
                Alumno.telefono.ilike(like),
                Alumno.email.ilike(like),
            )
        )
    alumnos = query.order_by(Alumno.apellido.asc(), Alumno.nombre.asc()).all()
    return render_template("alumnos/lista.html", alumnos=alumnos, q=q)


@alumnos_bp.route("/alumnos/nuevo")
def nuevo():
    return render_template(
        "alumnos/form.html",
        alumno_id=None,
        form_data={},
        errores=[],
    )


@alumnos_bp.route("/alumnos", methods=["POST"])
def crear():
    form_data = _form_data_from_request()
    nombre = form_data["nombre"]
    apellido = form_data["apellido"]
    telefono = form_data["telefono"]

    errores = _required_fields_missing(nombre, apellido, telefono)
    fecha_nacimiento = _parse_date(form_data["fecha_nacimiento"])
    edad = _parse_int(form_data["edad"])
    if not fecha_nacimiento and edad is None:
        errores.append("fecha_nacimiento")
        errores.append("edad")

    if errores:
        return render_template(
            "alumnos/form.html",
            alumno_id=None,
            form_data=form_data,
            errores=errores,
        )

    alumno = Alumno(
        nombre=nombre,
        apellido=apellido,
        fecha_nacimiento=fecha_nacimiento,
        edad=_age_from_date(fecha_nacimiento) if fecha_nacimiento else edad,
        signo_zodiaco=_zodiac_from_date(fecha_nacimiento)
        or form_data["signo_zodiaco"]
        or None,
        profesion=form_data["profesion"] or None,
        telefono=telefono,
        email=form_data["email"] or None,
        fuma=form_data["fuma"],
        patologias_fisicas=form_data["patologias_fisicas"] or None,
        patologias_psicologicas=form_data["patologias_psicologicas"] or None,
        toma_medicacion=form_data["toma_medicacion"],
        medicacion=form_data["medicacion"] or None,
        presion_sanguinea=form_data["presion_sanguinea"] or None,
        practica_yoga_previamente=form_data["practica_yoga_previamente"],
        motivo_practica=form_data["motivo_practica"] or None,
        realiza_actividad_fisica=form_data["realiza_actividad_fisica"],
        como_nos_conocio=form_data["como_nos_conocio"] or None,
        observaciones_generales=form_data["observaciones_generales"] or None,
    )
    db.session.add(alumno)
    db.session.commit()
    return redirect(url_for("alumnos.detalle", alumno_id=alumno.id))


@alumnos_bp.route("/alumnos/<int:alumno_id>")
def detalle(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
    return render_template("alumnos/detalle.html", alumno=alumno)


@alumnos_bp.route("/alumnos/<int:alumno_id>/pdf")
def pdf(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)

    pdf = _new_pdf()
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Historia Clínica - Alumno", ln=True)

    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Alumno: {alumno.apellido}, {alumno.nombre}", ln=True)
    pdf.cell(
        0,
        8,
        f"Fecha de nacimiento: {alumno.fecha_nacimiento or '-'}",
        ln=True,
    )
    pdf.cell(0, 8, f"Edad: {alumno.edad or '-'}", ln=True)
    pdf.cell(0, 8, f"Signo zodiacal: {alumno.signo_zodiaco or '-'}", ln=True)
    pdf.cell(0, 8, f"Teléfono: {alumno.telefono}", ln=True)
    pdf.cell(0, 8, f"Email: {alumno.email or '-'}", ln=True)
    pdf.cell(0, 8, f"Fecha de registro: {alumno.fecha_alta}", ln=True)
    pdf.ln(4)

    def section(title, lines):
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, title, ln=True)
        pdf.set_font("Helvetica", "", 11)
        for label, value in lines:
            _pdf_multiline(pdf, f"{label}: {value}", line_height=6)
        pdf.ln(2)

    section(
        "Salud general",
        [
            ("Fuma", "Si" if alumno.fuma else "No"),
            ("Presión sanguínea", alumno.presion_sanguinea or "-"),
            ("Patologías físicas", alumno.patologias_fisicas or "-"),
            ("Patologías psicológicas", alumno.patologias_psicologicas or "-"),
        ],
    )
    section(
        "Medicaciones",
        [
            ("Toma medicación", "Si" if alumno.toma_medicacion else "No"),
            ("Detalle", alumno.medicacion or "-"),
        ],
    )
    section(
        "Actividad física",
        [
            ("Practicó yoga", "Si" if alumno.practica_yoga_previamente else "No"),
            ("Actividad física", "Si" if alumno.realiza_actividad_fisica else "No"),
            ("Motivo", alumno.motivo_practica or "-"),
            ("Cómo nos conocio", alumno.como_nos_conocio or "-"),
        ],
    )
    section("Observaciones", [("Notas", alumno.observaciones_generales or "-")])

    pdf_bytes = _pdf_bytes(pdf)
    return (
        pdf_bytes,
        200,
        {
            "Content-Type": "application/pdf",
            "Content-Disposition": f"inline; filename=alumno_{alumno.id}.pdf",
        },
    )


@alumnos_bp.route("/alumnos/pdf")
def pdf_listado():
    alumnos = Alumno.query.order_by(Alumno.apellido.asc(), Alumno.nombre.asc()).all()

    pdf = _new_pdf()
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Listado de alumnos", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Fecha de emision: {date.today()}", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Alumno | Telefono | Fecha registro", ln=True)
    pdf.set_font("Helvetica", "", 11)
    for alumno in alumnos:
        nombre = f"{alumno.apellido}, {alumno.nombre}"
        line = f"{nombre} | {alumno.telefono} | {alumno.fecha_alta}"
        _pdf_multiline(pdf, line, line_height=6)

    pdf_bytes = _pdf_bytes(pdf)
    return (
        pdf_bytes,
        200,
        {
            "Content-Type": "application/pdf",
            "Content-Disposition": "inline; filename=alumnos_listado.pdf",
        },
    )


@alumnos_bp.route("/alumnos/<int:alumno_id>/editar")
def editar(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
    return render_template(
        "alumnos/form.html",
        alumno_id=alumno.id,
        form_data=_form_data_from_model(alumno),
        errores=[],
    )


@alumnos_bp.route("/alumnos/<int:alumno_id>", methods=["POST"])
def actualizar(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)

    form_data = _form_data_from_request()
    nombre = form_data["nombre"]
    apellido = form_data["apellido"]
    telefono = form_data["telefono"]

    errores = _required_fields_missing(nombre, apellido, telefono)
    fecha_nacimiento = _parse_date(form_data["fecha_nacimiento"])
    edad = _parse_int(form_data["edad"])
    if not fecha_nacimiento and edad is None:
        errores.append("fecha_nacimiento")
        errores.append("edad")

    if errores:
        return render_template(
            "alumnos/form.html",
            alumno_id=alumno.id,
            form_data=form_data,
            errores=errores,
        )

    alumno.nombre = nombre
    alumno.apellido = apellido
    alumno.fecha_nacimiento = fecha_nacimiento
    alumno.edad = _age_from_date(fecha_nacimiento) if fecha_nacimiento else edad
    alumno.signo_zodiaco = _zodiac_from_date(fecha_nacimiento) or form_data[
        "signo_zodiaco"
    ] or None
    alumno.profesion = form_data["profesion"] or None
    alumno.telefono = telefono
    alumno.email = form_data["email"] or None
    alumno.fuma = form_data["fuma"]
    alumno.patologias_fisicas = form_data["patologias_fisicas"] or None
    alumno.patologias_psicologicas = form_data["patologias_psicologicas"] or None
    alumno.toma_medicacion = form_data["toma_medicacion"]
    alumno.medicacion = form_data["medicacion"] or None
    alumno.presion_sanguinea = form_data["presion_sanguinea"] or None
    alumno.practica_yoga_previamente = form_data["practica_yoga_previamente"]
    alumno.motivo_practica = form_data["motivo_practica"] or None
    alumno.realiza_actividad_fisica = form_data["realiza_actividad_fisica"]
    alumno.como_nos_conocio = form_data["como_nos_conocio"] or None
    alumno.observaciones_generales = form_data["observaciones_generales"] or None

    db.session.commit()
    return redirect(url_for("alumnos.detalle", alumno_id=alumno.id))


@alumnos_bp.route("/alumnos/<int:alumno_id>/eliminar", methods=["POST"])
def eliminar(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
    db.session.delete(alumno)
    db.session.commit()
    return redirect(url_for("alumnos.listar"))
