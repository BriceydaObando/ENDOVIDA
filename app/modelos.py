
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
            ORDER BY id_paciente
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
            SELECT s.id_seguimiento, p.nombre, p.apellido,
                   ps.nombre, ps.apellido, s.fecha,
                   s.observacion, s.estado
            FROM SEGUIMIENTO s
            INNER JOIN PACIENTES p
                ON s.id_paciente = p.id_paciente
            INNER JOIN PERSONAL_SALUD ps
                ON s.id_personal = ps.id_personal
            ORDER BY s.id_seguimiento
        """)
        return cursor.fetchall()
    finally:
        conexion.close()


def obtener_personal_salud():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        ejecutar_consulta(cursor, """
            SELECT id_personal, nombre, apellido
            FROM PERSONAL_SALUD
            ORDER BY nombre
        """)
        return cursor.fetchall()
    finally:
        conexion.close()


def registrar_seguimiento(id_paciente, id_personal, fecha, observacion, estado):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        ejecutar_consulta(cursor, """
            INSERT INTO SEGUIMIENTO
            (id_paciente, id_personal, fecha, observacion, estado)
            VALUES (?, ?, ?, ?, ?)
        """, (id_paciente, id_personal, fecha, observacion, estado))
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
            SELECT r.id_reporte, p.nombre, p.apellido,
                   r.fecha, r.tiempo_reporte, r.descripcion
            FROM REPORTE r
            INNER JOIN PACIENTES p
                ON r.id_paciente = p.id_paciente
            ORDER BY r.id_reporte
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


def eliminar_usuario(id_usuario):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        ejecutar_consulta(
            cursor,
            "DELETE FROM USUARIOS WHERE id_usuario = ?",
            (id_usuario,)
        )
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def obtener_usuarios():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        ejecutar_consulta(cursor, """
            SELECT id_usuario, usuario
            FROM USUARIOS
            ORDER BY id_usuario
        """)
        return cursor.fetchall()
    finally:
        conexion.close()
