from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Cargar el archivo de Excel y seleccionar las columnas usando índices en lugar de letras
df = pd.read_excel('datos/base_de_datos.xlsx', header=None)
df = df.iloc[:, [0, 2, 3, 5]]  # Seleccionar las columnas por índice (0: A, 2: C, 3: D, 5: F)
df.columns = ["codigo", "autor", "titulo", "año"]  # Renombrar columnas

# Asegurarse de que las columnas sean cadenas (para evitar errores al usar str.contains)
df = df.fillna('').astype(str)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    criterio = request.form.get('criterio')
    termino = request.form.get('termino', '').strip()  # Eliminar espacios adicionales

    # Verificar que el término no esté vacío
    if not termino:
        return jsonify({"error": "El término de búsqueda no puede estar vacío"}), 400

    # Filtrar los resultados del DataFrame basado en el criterio de búsqueda
    if criterio in ["codigo", "autor", "titulo"]:
        resultados = df[df[criterio].str.contains(termino, case=False, na=False)]
    else:
        return jsonify({"error": "Criterio de búsqueda no válido"}), 400

    # Seleccionar solo las columnas necesarias en el resultado
    resultados = resultados[['codigo', 'autor', 'titulo', 'año']]
    
    # Convertir resultados a diccionario para enviarlos como JSON
    resultados_dict = resultados.to_dict(orient='records')
    
    return jsonify(resultados_dict)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
