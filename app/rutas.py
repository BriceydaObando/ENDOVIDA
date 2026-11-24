
from datetime import date
from functools import wraps

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session
)
from werkzeug.security import check_password_hash

from app import app
from app.conexion import obtener_conexion, ejecutar_consulta
from app.modelos import (
    obtener_pacientes,
    registrar_paciente,
    obtener_seguimientos,
    obtener_reportes,
    registrar_usuario,
    obtener_personal_salud,
    registrar_seguimiento,
    registrar_reporte
)


def login_requerido(funcion):
    @wraps(funcion)
    def decorada(*args, **kwargs):
        if "id_usuario" not in session:
            return redirect(url_for("login"))

        return funcion(*args, **kwargs)

    return decorada


@app.route("/")
def inicio():
    return render_template("inicio.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "")

        conexion = obtener_conexion()

        try:
            cursor = conexion.cursor()

            ejecutar_consulta(cursor, """
                SELECT id_usuario, usuario, contrasena
                FROM USUARIOS
                WHERE usuario = ?
            """, (usuario,))

            usuario_encontrado = cursor.fetchone()

        finally:
            conexion.close()

        if (
            usuario_encontrado
            and check_password_hash(
                usuario_encontrado[2],
                contrasena
            )
        ):
            session.clear()
            session["id_usuario"] = usuario_encontrado[0]
            session["usuario"] = usuario_encontrado[1]

            return redirect(url_for("inicio"))

        return render_template(
            "login.html",
            mensaje="Usuario o contraseña incorrectos."
        )

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/registro", methods=["GET", "POST"])
@login_requerido
def registro():

    if request.method == "POST":

        usuario = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "")

        if not usuario or not contrasena:
            return render_template(
                "registro.html",
                mensaje="Completa todos los campos."
            )

        registrar_usuario(usuario, contrasena)

        return redirect(url_for("login"))

    return render_template("registro.html")


@app.route("/pacientes", methods=["GET", "POST"])
@login_requerido
def pacientes():

    if request.method == "POST":

        nombre = request.form["nombre"].strip()
        apellido = request.form["apellido"].strip()
        documento = request.form["documento"].strip()
        edad = request.form["edad"]
        correo = request.form["correo"].strip()
        telefono = request.form["telefono"].strip()

        registrar_paciente(
            nombre,
            apellido,
            documento,
            edad,
            correo,
            telefono
        )

    pacientes = obtener_pacientes()

    return render_template(
        "pacientes.html",
        pacientes=pacientes
    )


@app.route("/seguimiento", methods=["GET", "POST"])
@login_requerido
def seguimiento():

    mensaje = None

    if request.method == "POST":

        try:
            id_paciente = int(request.form["id_paciente"])
            id_personal = int(request.form["id_personal"])
            fecha = date.fromisoformat(request.form["fecha"])
            observaciones = request.form["observaciones"].strip()
            estado = request.form["estado"]

            if not observaciones:
                raise ValueError

            registrar_seguimiento(
                id_paciente,
                id_personal,
                fecha,
                observaciones,
                estado
            )

            mensaje = "Seguimiento registrado correctamente."

        except ValueError:
            mensaje = (
                "Verifica los datos del formulario "
                "e intenta nuevamente."
            )

    pacientes = obtener_pacientes()
    personal = obtener_personal_salud()
    seguimientos = obtener_seguimientos()

    return render_template(
        "seguimiento.html",
        pacientes=pacientes,
        personal=personal,
        seguimientos=seguimientos,
        mensaje=mensaje
    )


@app.route("/reportes", methods=["GET", "POST"])
@login_requerido
def reportes():

    mensaje = None

    if request.method == "POST":

        try:
            id_paciente = int(request.form["id_paciente"])
            fecha = date.fromisoformat(request.form["fecha"])
            tiempo_reporte = request.form["tiempo_reporte"].strip()
            descripcion = request.form["descripcion"].strip()

            if not tiempo_reporte or len(tiempo_reporte) > 50:
                raise ValueError

            if not descripcion:
                raise ValueError

            registrar_reporte(
                id_paciente,
                fecha,
                tiempo_reporte,
                descripcion
            )

            mensaje = "Reporte registrado correctamente."

        except ValueError:
            mensaje = (
                "Verifica los datos del formulario "
                "e intenta nuevamente."
            )

    pacientes = obtener_pacientes()
    reportes = obtener_reportes()

    return render_template(
        "reportes.html",
        pacientes=pacientes,
        reportes=reportes,
        mensaje=mensaje
    )
