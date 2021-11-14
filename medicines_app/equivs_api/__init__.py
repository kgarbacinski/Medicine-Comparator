from flask import Flask
from flask_marshmallow import Marshmallow
from flask_cors import CORS
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    ma.init_app(app=app)
    CORS(app)
    from medicines_app.equivs_api.search_api import get_equivalents_blueprint, livesearch_blueprint, index_blueprint
    app.register_blueprint(get_equivalents_blueprint)
    app.register_blueprint(livesearch_blueprint)
    app.register_blueprint(index_blueprint)

    return app


if __name__ == '__main__':
    port = 5001
    create_app().run(host ="0.0.0.0", port=port, debug=True)
