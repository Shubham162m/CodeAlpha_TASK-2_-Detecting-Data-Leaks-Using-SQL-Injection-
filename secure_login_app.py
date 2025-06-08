from flask import Flask, request, jsonify, render_template
import mysql.connector
from cryptography.fernet import Fernet
import os

app = Flask(__name__)

KEY = Fernet.generate_key()
cipher = Fernet(KEY)

db = mysql.connector.connect(
    host="localhost",
    user="app_user",
    password="SimplePass123",
    database="secure_app"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username'].replace("'", "")  
    password = cipher.encrypt(data['password'].encode()).decode()  
    
    cursor = db.cursor(prepared=True)
    sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(sql, (username, password))
    db.commit()
    
    return jsonify({"message": "User created safely!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username'].replace("'", "")
    
    cursor = db.cursor(prepared=True)
    sql = "SELECT password FROM users WHERE username = %s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()
    
    if result and data['password'] == cipher.decrypt(result[0].encode()).decode():
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"error": "Invalid login"}), 401

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    if not os.path.exists('templates/index.html'):
        with open('templates/index.html', 'w') as f:
            f.write('''<!DOCTYPE html>
<html>
<head>
    <title>Secure Login System</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 500px; margin: 0 auto; padding: 20px; }
        form { margin-bottom: 30px; border: 1px solid #ddd; padding: 20px; border-radius: 5px; }
        input { display: block; margin: 10px 0; padding: 8px; width: 95%; }
        button { padding: 8px 15px; background: #007bff; color: white; border: none; border-radius: 4px; }
        #result { margin-top: 20px; padding: 10px; border-radius: 4px; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <h1>Secure Login System</h1>
    
    <h2>Register</h2>
    <form id="registerForm">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Register</button>
    </form>

    <h2>Login</h2>
    <form id="loginForm">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>

    <div id="result"></div>
    <div id="result"></div>

    <script>
        function showResult(message, isError = false) {
            const resultDiv = document.getElementById('result');
            resultDiv.textContent = typeof message === 'object' 
                ? JSON.stringify(message, null, 2) 
                : message;
            resultDiv.className = isError ? 'error' : 'success';
        }

        document.getElementById('registerForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            
            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        username: formData.get('username'),
                        password: formData.get('password')
                    })
                });
                const data = await response.json();
                showResult(data, !response.ok);
            } catch (error) {
                showResult(error.message, true);
            }
        });

        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        username: formData.get('username'),
                        password: formData.get('password')
                    })
                });
                const data = await response.json();
                showResult(data, !response.ok);
            } catch (error) {
                showResult(error.message, true);
            }
        });
    </script>
</body>
</html>''')
    
    app.run(debug=True)