from flask import render_template,Flask
from flask_login import current_user

def errors(app:Flask):

    #404
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("error.html") , 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("error.html") , 500  #pragma: no cover , not testable

    @app.errorhandler(403)
    def page_forbidden(error):
        return render_template("error.html") , 403
    
    @app.errorhandler(400)
    def bad_request(error):
        return render_template("error.html"), 400