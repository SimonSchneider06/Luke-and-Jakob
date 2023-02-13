from flask import render_template
from flask_login import current_user

def errors(app):

    #404
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("error.html",user = current_user) , 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("error.html",user = current_user) , 500

    @app.errorhandler(403)
    def page_forbidden(error):
        return render_template("error.html",user = current_user) , 403