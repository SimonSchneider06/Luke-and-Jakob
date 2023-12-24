from website import create_app
import os

app = create_app(os.getenv("FLASK_CONFIG") or "ionos")


if __name__ == '__main__':
    app.run(host = "0.0.0.0",port = 5000,debug = False)   # for google login and https: add 'ssl_context = "adhoc"' as parameter in app.run

else:
    gunicorn = create_app(os.getenv("FLASK_CONFIG") or "ionos")