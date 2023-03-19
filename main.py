
from flask import Flask
from app.views import main_blueprint

app = Flask(__name__)
app.register_blueprint(main_blueprint)
app.register_blueprint(books_blueprint)

if __name__ == "__main__":
    app.run()