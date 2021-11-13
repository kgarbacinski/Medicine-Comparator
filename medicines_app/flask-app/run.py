from flask_application.main import create_app


app = create_app()

if __name__ == "__main__":
    port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)
