from flask import Flask, render_template_string, request
import webbrowser
import os

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Browser Control</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #00c6ff);
            background-size: 400% 400%;
            animation: gradient 12s ease infinite;
            font-family: Arial, sans-serif;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .card {
            width: 400px;
            padding: 40px;
            border-radius: 25px;
            text-align: center;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            box-shadow: 0 0 40px rgba(0,0,0,0.5);
            animation: float 3s ease-in-out infinite;
        }

        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }

        h1 {
            color: white;
            font-size: 42px;
            margin-bottom: 30px;
            animation: glow 2s infinite alternate;
        }

        @keyframes glow {
            from {
                text-shadow: 0 0 10px #00f7ff;
            }
            to {
                text-shadow: 0 0 25px #ff00ff;
            }
        }

        .btn {
            width: 250px;
            padding: 15px;
            margin: 15px;
            border: none;
            border-radius: 15px;
            font-size: 20px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }

        .open {
            background: #00ff88;
            color: black;
        }

        .open:hover {
            transform: scale(1.1);
            box-shadow: 0 0 20px #00ff88;
        }

        .close {
            background: #ff004c;
            color: white;
        }

        .close:hover {
            transform: scale(1.1);
            box-shadow: 0 0 20px #ff004c;
        }

        p {
            color: white;
            opacity: 0.8;
        }
    </style>
</head>
<body>

<div class="card">
    <h1>WELCOME</h1>
    <p>Beautiful Browser Controller</p>

    <form method="POST" action="/open">
        <button class="btn open">OPEN BROWSER</button>
    </form>

    <form method="POST" action="/close">
        <button class="btn close">CLOSE BROWSER</button>
    </form>
</div>

</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/open', methods=['POST'])
def open_browser():
    webbrowser.open('https://www.google.com')
    return render_template_string(HTML)

@app.route('/close', methods=['POST'])
def close_browser():

    # Windows
    os.system('taskkill /F /IM chrome.exe >nul 2>&1')
    os.system('taskkill /F /IM msedge.exe >nul 2>&1')
    os.system('taskkill /F /IM firefox.exe >nul 2>&1')

    # Linux
    os.system('pkill chrome')
    os.system('pkill firefox')

    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
