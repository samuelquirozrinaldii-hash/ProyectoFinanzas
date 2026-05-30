# Control de Finanzas Personales 💰

Este es un gestor de ingresos y gastos desarrollado en Python. El proyecto nació con la idea de tener un control real y ordenado del dinero, permitiendo guardar transacciones, calcular balances automáticamente y almacenar todo de forma local.

Lo diseñé con una arquitectura limpia (separando la base de datos, las funciones de control y las vistas) y cuenta con dos formas de uso: una interfaz rápida por consola y una interfaz gráfica de escritorio.

## 🚀 Características principales
* **Registro completo:** Guarda ingresos o gastos asignando monto, categoría (comida, ropa, etc.), descripción y fecha automática.
* **Cálculo de Balance Neto:** Muestra el total de lo que entra, lo que sale y si estás en saldo verde o rojo.
* **Historial Interactivo:** Una tabla visual (Treeview) donde puedes hacer clic en cualquier registro para cargarlo, editarlo o eliminarlo permanentemente.
* **Base de datos local:** Usa SQLite3, por lo que no necesitas internet ni configurar servidores externos para que funcione.

## 🛠️ Tecnologías utilizadas
* **Python 3**
* **Tkinter & ttk** (Para el diseño de la interfaz de escritorio)
* **SQLite3** (Para la persistencia de los datos)

## 📦 Estructura del repositorio
* `Conexion.py`: Configuración inicial y creación de las tablas de la base de datos.
* `Funciones.py`: Toda la lógica del sistema (Registrar, Ver, Calcular Balance, Editar y Eliminar).
* `Interfaz.py`: La aplicación visual con ventanas, botones y tablas interactivas.
* `main.py`: La versión alternativa para gestionar todo directamente desde la terminal.

---

## 💻 Cómo probar el proyecto

1. **Clonar el repositorio o descargar los archivos:**
   ```bash
   git clone [https://github.com/samuelquirozrinaldii-hash/Proyecto-Control-Finanzas.git](https://github.com/samuelquirozrinaldii-hash/Proyecto-Control-Finanzas.git)
   cd Proyecto-Control-Finanzas
