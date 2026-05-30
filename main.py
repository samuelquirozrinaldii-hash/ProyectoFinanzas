from Conexion import crear_tabla
import Funciones as crud
from datetime import date

def menu():
    crear_tabla()
    
    while True:
        print("\n---GESTOR DE FINANZAS PERSONALES---")
        print("1. Registrar Ingreso / Gasto")
        print("2. Ver Historial de Transacciones")
        print("3. Ver Balance General")
        print("4. Editar Transacción")
        print("5. Eliminar Transacción")
        print("6. Salir")
        
        opcion = input("Selecciona una opcion: ")
        
        if opcion == "1":
            tipo = input("Es Ingreso o Gasto?: ").strip().capitalize()
            monto = float(input("Monto ($): "))
            categoria = input("Categoria (Comida, Sueldo, Ropa): ").strip().capitalize()
            fecha_hoy = date.today().strftime("%Y-%m-%d")
            descripcion = input("Descripcion: ")
            
            crud.registrar_transaccion(tipo, monto, categoria, fecha_hoy, descripcion)
            
        elif opcion == "2":
            print("\n---HISTORIAL---")
            transacciones = crud.ver_transacciones()
            print(f"{'ID':<4} | {'Tipo':<8} | {'Monto':<10} | {'Categoría':<12} | {'Fecha':<12} | {'Descripción'}")
            print("-" * 70)
            for t in transacciones:
                print(f"{t[0]:<4} | {t[1]:<8} | ${t[2]:<9} | {t[3]:<12} | {t[4]:<12} | {t[5]}")
                
        elif opcion == "3":
            ingresos, gastos, balance = crud.obtener_balance()
            print("\n---BALANCE GENERAL---")
            print(f"Total Ingresos: ${ingresos:.2f}")
            print(f"Total Gastos: ${gastos:.2f}")
            print(f"Balance Neto: ${balance:.2f}")
            if balance < 0:
                print("Estás gastando más de lo que ganas. Ojo con eso ")
                
        elif opcion == "4":
            id_reg = int(input("Introduce el ID del registro a editar: "))
            nuevo_m = float(input("Nuevo Monto $$$: "))
            nueva_cat = input("Nueva Categoría: ").strip().capitalize()
            crud.actualizar_transaccion(id_reg, nuevo_m, nueva_cat)
            
        elif opcion == "5":
            id_reg = int(input("Introduce el ID del registro a eliminar: "))
            confirmar = input(f"¿Seguro que quieres borrar el ID {id_reg}? (s/n): ")
            if confirmar.lower() == 's':
                crud.eliminar_transaccion(id_reg)
                
        elif opcion == "6":
            print("\nGracias por usar el gestor de Finanzas!")
            break
        else:
            print("Error. Intenta de nuevo.")

if __name__ == "__main__":
    menu()
