from waitress import serve
from wallet import app  # assuming "app" is the Flask app object in wallet.py

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
