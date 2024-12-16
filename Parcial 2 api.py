from flask import Flask, jsonify, request
import pandas as pd

# Crear aplicación Flask
app = Flask(__name__)

# Cargar y procesar los datos
file_path = 'API_SH.IMM.MEAS_DS2_en_csv_v2_787.csv'  # Asegúrate de que la ruta del archivo sea correcta
data = pd.read_csv(file_path, skiprows=4)

# Filtrar los datos para Panamá
panama_data = data[data['Country Name'] == 'Panama']
panama_data_cleaned = panama_data.drop(columns=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code', 'Unnamed: 68'])
panama_data_long = panama_data_cleaned.melt(var_name="Year", value_name="Measles Vaccination Rate")

# Preparar los datos para la API
panama_data_prepared = [
    {"year": int(row["Year"]), "vaccination_rate": row["Measles Vaccination Rate"]}
    for _, row in panama_data_long.iterrows() if not pd.isna(row["Measles Vaccination Rate"])
]

# Endpoint 1: Obtener todos los datos
@app.route('/vaccination', methods=['GET'])
def get_all_data():
    return jsonify(panama_data_prepared)

# Endpoint 2: Obtener datos de un año específico
@app.route('/vaccination/<int:year>', methods=['GET'])
def get_data_by_year(year):
    result = next((item for item in panama_data_prepared if item['year'] == year), None)
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Data not found for the requested year."}), 404

# Endpoint 3: Obtener datos de un rango de años
@app.route('/vaccination/range', methods=['GET'])
def get_data_by_range():
    start_year = request.args.get('start', type=int)
    end_year = request.args.get('end', type=int)

    if start_year is None or end_year is None:
        return jsonify({"error": "Please provide both start and end years."}), 400

    result = [item for item in panama_data_prepared if start_year <= item['year'] <= end_year]
    return jsonify(result)

# Correr la aplicación
if __name__ == '__main__':
    app.run(debug=True)
