from flask import Flask
from models import db
from routes.auth_routes import auth
from routes.task_routes import task
from routes.project_routes import project

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.secret_key = "secret"

db.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(task)
app.register_blueprint(project)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)