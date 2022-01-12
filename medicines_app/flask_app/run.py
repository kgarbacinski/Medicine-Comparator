from flask_application.main import create_app, db
# from medicines_app.flask_app.flask_application.models import add_tokens, Token
# import os

app = create_app()

if __name__ == "__main__":
    port = 5000
    app.run(host="0.0.0.0", port=port, debug=True)
