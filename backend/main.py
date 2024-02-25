from flask import Flask
from src.backend.routes.dane_scraper_routes import dian_methods


app = Flask(__name__)

app.register_blueprint(dian_methods)



if __name__ == "__main__":
     
     app.run(host="0.0.0.0", debug=True, port=5000)
