import sqlite3
def conectar():
    return sqlite3.connect("finanzas_personales.db")

def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,         
            monto REAL NOT NULL,        
            categoria TEXT NOT NULL,    
            fecha TEXT NOT NULL,        
            descripcion TEXT
        )
    """)
    
    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    crear_tabla()
    print("¡Base de datos y tabla preparadas exitosamente!")
