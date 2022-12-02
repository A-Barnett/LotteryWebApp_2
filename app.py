# IMPORTS
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# CONFIG
app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lottery.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialise database
db = SQLAlchemy(app)


# HOME PAGE VIEW
@app.route('/')
def index():
    return render_template('main/index.html')


# BLUEPRINTS
# import blueprints
from users.views import users_blueprint
from admin.views import admin_blueprint
from lottery.views import lottery_blueprint
#
# # register blueprints with app
app.register_blueprint(users_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(lottery_blueprint)

@app.errorhandler(400)
def error_400(error):
    return render_template('Errors/400.html'), 400

@app.errorhandler(403)
def error_403(error):
    return render_template('Errors/403.html'), 403


@app.errorhandler(404)
def error_404(error):
    return render_template('Errors/404.html'), 404


@app.errorhandler(500)
def error_500(error):
    return render_template('Errors/500.html'), 500

@app.errorhandler(503)
def error_503(error):
    return render_template('Errors/503.html'), 503


if __name__ == "__main__":
    app.run()
