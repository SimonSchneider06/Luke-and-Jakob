from website import create_app
import os

app = create_app(os.getenv("FLASK_CONFIG") or "default")


if __name__ == '__main__':
    app.run(host = "0.0.0.0",port = 5000,debug = True)   # for google login and https: add 'ssl_context = "adhoc"' as parameter in app.run