from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../models/medicine.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app=app)
    ma.init_app(app=app)

    from equivs_api.search_api import get_reference_drug_blueprint, livesearch_blueprint, index_blueprint
    app.register_blueprint(get_reference_drug_blueprint)
    app.register_blueprint(livesearch_blueprint)
    app.register_blueprint(index_blueprint)

    return app


if __name__ == '__main__':
    port = 3000
    create_app().run(host='0.0.0.0', port=port, debug=True)
