from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configurazione di MariaDB
db_config = {
    'user': 'flask_user',
    'password': 'your_password',
    'host': 'localhost',
    'database': 'sensor_data_db'
}

@app.route('/send-data', methods=['POST'])
def receive_data():
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400

    luminosity = data.get("luminosity")
    number = data.get("number")

    if luminosity is None or number is None:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO sensor_data (luminosity, number) VALUES (%s, %s)"
        cursor.execute(query, (luminosity, number))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    return jsonify({"message": "Data saved successfully"}), 200

@app.route('/get-data', methods=['GET'])
def get_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "SELECT * FROM sensor_data"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        data = [
            {"id": row[0], "luminosity": row[1], "number": row[2], "timestamp": row[3]}
            for row in rows
        ]
        return jsonify(data), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)