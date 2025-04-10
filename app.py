from flask import Flask, request, jsonify, render_template, url_for
import threading
import webbrowser
import launcher

app = Flask(__name__)

# Home route serves the login page
@app.route('/')
def home():
    return render_template('index.html')

# API route for login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Dummy credentials (replace with real DB check)
    if username == "admin" and password == "123":
        launcher.launch_gui()
        return jsonify({"status": "success", "message": "Login successful."})
    else:
        return jsonify({"status": "fail", "message": "Invalid credentials."}), 401

# Automatically open browser
def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

# Run the app
if __name__ == '__main__':
    threading.Timer(1.25, open_browser).start()
    app.run(debug=True)
