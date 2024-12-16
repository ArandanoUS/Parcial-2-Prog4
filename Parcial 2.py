from flask import Flask, render_template
import requests

# Crear la aplicación principal
app = Flask(__name__)

# URL base de la API (asumiendo que está en localhost y en el puerto 5000)
API_BASE_URL = 'http://localhost:5000/vaccination'

# Ruta principal de la aplicación
@app.route('/')
def home():
    try:
        # Llamar a la API para obtener todos los datos
        response = requests.get(API_BASE_URL)
        data = response.json()
        return render_template('home.html', data=data)
    except Exception as e:
        return f"Error al conectar con la API: {str(e)}"

# Ruta para mostrar datos de un año específico
@app.route('/year/<int:year>')
def year_data(year):
    try:
        # Llamar a la API para obtener datos de un año
        response = requests.get(f"{API_BASE_URL}/{year}")
        if response.status_code == 404:
            return render_template('error.html', message="Datos no encontrados para el año solicitado.")
        data = response.json()
        return render_template('year.html', data=data)
    except Exception as e:
        return f"Error al conectar con la API: {str(e)}"

# Ruta para mostrar datos de un rango de años
@app.route('/range')
def range_data():
    # Obtener los parámetros de rango desde la consulta (ejemplo: /range?start=2000&end=2020)
    start_year = requests.args.get('start', type=int)
    end_year = requests.args.get('end', type=int)

    if start_year is None or end_year is None:
        return render_template('error.html', message="Por favor, proporciona los años de inicio y fin.")

    try:
        # Llamar a la API para obtener datos de rango
        response = requests.get(f"{API_BASE_URL}/range?start={start_year}&end={end_year}")
        data = response.json()
        return render_template('range.html', data=data, start=start_year, end=end_year)
    except Exception as e:
        return f"Error al conectar con la API: {str(e)}"

# Correr la aplicación
if __name__ == '__main__':
    app.run(debug=True)
