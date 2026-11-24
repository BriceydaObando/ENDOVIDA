
from app.conexion import obtener_conexion, ejecutar_consulta
from werkzeug.security import generate_password_hash


def obtener_pacientes():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        ejecutar_consulta(cursor, """
            SELECT id_paciente, nombre, apellido, documento,
                   edad, correo, telefono
            FROM PACIENTES
        """)
        return cursor.fetchall()
    finally:
        conexion.close()


def registrar_paciente(nombre, apellido, documento, edad, correo, telefono):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        ejecutar_consulta(cursor, """
            INSERT INTO PACIENTES
            (nombre, apellido, documento, edad, correo, telefono)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, apellido, documento, edad, correo, telefono))
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def obtener_seguimientos():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        ejecutar_consulta(cursor, """
            SELECT id_seguimiento, id_paciente, id_personal,
                   fecha, observaciones, estado
            FROM SEGUIMIENTO
        """)
        return cursor.fetchall()
    finally:
        conexion.close()


def obtener_personal_salud():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        ejecutar_consulta(cursor, """
            SELECT id_personal, nombre, apellido, cargo
            FROM PERSONAL_SALUD
        """)
        return cursor.fetchall()
    finally:
        conexion.close()


def registrar_seguimiento(id_paciente, id_personal, fecha, observaciones, estado):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        ejecutar_consulta(cursor, """
            INSERT INTO SEGUIMIENTO
            (id_paciente, id_personal, fecha, observaciones, estado)
            VALUES (?, ?, ?, ?, ?)
        """, (id_paciente, id_personal, fecha, observaciones, estado))
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def obtener_reportes():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        ejecutar_consulta(cursor, """
            SELECT id_reporte, id_paciente, fecha,
                   tiempo_reporte, descripcion
            FROM REPORTE
        """)
        return cursor.fetchall()
    finally:
        conexion.close()


def registrar_reporte(id_paciente, fecha, tiempo_reporte, descripcion):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        ejecutar_consulta(cursor, """
            INSERT INTO REPORTE
            (id_paciente, fecha, tiempo_reporte, descripcion)
            VALUES (?, ?, ?, ?)
        """, (id_paciente, fecha, tiempo_reporte, descripcion))
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def registrar_usuario(usuario, contrasena):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        contrasena_protegida = generate_password_hash(contrasena)
        ejecutar_consulta(cursor, """
            INSERT INTO USUARIOS (usuario, contrasena)
            VALUES (?, ?)
        """, (usuario, contrasena_protegida))
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
