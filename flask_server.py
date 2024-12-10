from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Ayush2001#@',
        database='Whatsapp_chat_analyzer'
    )
    return connection

@app.route('/sign_up', methods=['POST'])
def sign_up():
    data = request.json
    username = data['username']
    password = data['password']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'User signed up successfully!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user:
        return jsonify({'message': 'Login successful!'})
    else:
        return jsonify({'message': 'Invalid username or password.'}), 401

@app.route('/test_db', methods=['GET'])
def test_db_connection():
    try:
        connection = get_db_connection()
        if connection.is_connected():
            return jsonify({"message": "Successfully connected to the database"}), 200
        else:
            return jsonify({"message": "Failed to connect to the database"}), 500
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
