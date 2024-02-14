from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

# Parámetros de conexión
server = '10.211.0.21'  # Reemplaza con el nombre de tu servidor SQL Server
database = 'TEA'  # Reemplaza con el nombre de tu base de datos
username = 'FLGWEB'  # Reemplaza con tu nombre de usuario
password = 'Fligosweb2014'  # Reemplaza con tu contraseña

# Cadena de conexión
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def search():
    try:
        # Establecer la conexión
        connection = pyodbc.connect(conn_str)

        # Crear un objeto cursor para ejecutar consultas SQL
        cursor = connection.cursor()

        # Obtener el ID ingresado por el usuario desde el formulario
        id = request.form['id']

        # Ejemplo de consulta SELECT con parámetro de ID y seleccionando solo los campos NOMBRE y VALOR
        select_query = "SELECT NOMBRE, VALOR FROM VX_CATALOGO_CONSULTA_PRECIOS_ALMACEN WHERE CODIGO = ?"

        # Ejecutar la consulta SELECT con el parámetro de ID
        cursor.execute(select_query, id)

        # Obtener los resultados de la consulta
        row = cursor.fetchone()

        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        # Renderizar la plantilla HTML con el resultado de la consulta
        if row:
            # Si se encuentra una fila, devolver los campos NOMBRE y VALOR
            nombre, valor = row
            return render_template('index.html', row={'NOMBRE': nombre, 'VALOR': valor}, no_result=False)
        else:
            # Si no se encuentra ninguna fila, devolver None y establecer no_result a True
            return render_template('index.html', row=None, no_result=True)

    except pyodbc.Error as e:
        return f"Error de conexión o consulta: {e}"


if __name__ == '__main__':
    app.run(debug=True)
