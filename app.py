from flask import Flask, render_template, request, redirect, url_for
import pyodbc

# Creación de una instancia de la aplicación Flask
app = Flask(__name__)

# Configuración de la conexión a la base de datos Access
# Asegúrate de reemplazar la ruta con la ubicación correcta de tu archivo .accdb
conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                      r'DBQ=C:\Users\ASUS\Documents\GitHub\buenas practicas\Taller\TasksDB.accdb;')

# Ruta principal de la aplicación
@app.route('/')
def index():
    """
    Ruta principal que muestra las tareas disponibles y enlace para agregar nuevas tareas.
    """
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Tareas')
    tareas = cursor.fetchall()
    return render_template('index.html', tareas=tareas)

# Ruta para agregar una nueva tarea
@app.route('/agregar_tarea', methods=['POST'])
def agregar_tarea():
    """
    Ruta que permite agregar una nueva tarea a la base de datos.
    """
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        estado = 0  # 0 representa "no completado"
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Tareas (descripcion, estado) VALUES (?, ?)', (descripcion, estado))
        conn.commit()
    return redirect(url_for('index'))

# Ruta para marcar una tarea como completada
@app.route('/completar_tarea/<int:Id>')
def completar_tarea(Id):
    """
    Ruta que permite marcar una tarea como completada.
    """
    cursor = conn.cursor()
    cursor.execute('UPDATE Tareas SET estado = 1 WHERE Id = ?', (Id,))
    conn.commit()
    return redirect(url_for('index'))

# Ruta para eliminar una tarea
@app.route('/eliminar_tarea/<int:Id>')
def eliminar_tarea(Id):
    """
    Ruta que permite eliminar una tarea.
    """
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Tareas WHERE Id = ?', (Id,))
    conn.commit()
    return redirect(url_for('index'))

# Verifica si el script se está ejecutando como el programa principal
if __name__ == '__main__':
    # Inicia la aplicación Flask en modo de depuración (debug)
    app.run(debug=True)

