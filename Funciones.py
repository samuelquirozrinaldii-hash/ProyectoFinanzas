import sqlite3
from Conexion import conectar

def registrar_transaccion(tipo, monto, categoria, fecha, descripcion):
    conn = conectar()
    cursor = conn.cursor()
    query = "INSERT INTO transacciones (tipo, monto, categoria, fecha, descripcion) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(query, (tipo, monto, categoria, fecha, descripcion))
    conn.commit()
    conn.close()
    print(f"\n{tipo} registrado correctamente.")

def ver_transacciones():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacciones ORDER BY fecha DESC")
    filas = cursor.fetchall()
    conn.close()
    return filas

def obtener_balance():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(monto) FROM transacciones WHERE tipo = 'Ingreso'")
    ingresos = cursor.fetchone()[0] or 0.0
    
    cursor.execute("SELECT SUM(monto) FROM transacciones WHERE tipo = 'Gasto'")
    gastos = cursor.fetchone()[0] or 0.0
    
    conn.close()
    return ingresos, gastos, (ingresos - gastos)

def actualizar_transaccion(id_registro, nuevo_monto, nueva_categoria):
    conn = conectar()
    cursor = conn.cursor()
    query = "UPDATE transacciones SET monto = ?, categoria = ? WHERE id = ?"
    cursor.execute(query, (nuevo_monto, nueva_categoria, id_registro))
    conn.commit()
    conn.close()
    print(f"\nRegistro ID {id_registro} actualizado.")

def eliminar_transaccion(id_registro):
    conn = conectar()
    cursor = conn.cursor()
    query = "DELETE FROM transacciones WHERE id = ?"
    cursor.execute(query, (id_registro,))
    conn.commit()
    conn.close()
    print(f"\nRegistro ID {id_registro} eliminado.")
