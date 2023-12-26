from flask import Flask, render_template, redirect, url_for, session
from flask_restful import Api
from models import db
from forms import LoginForm, UpdateForm
from services import GuestService
from api import *

app = Flask(__name__)
api = Api(api_bp)

app.config['SECRET_KEY'] = 'YourSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/french_resort'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api.add_resource(LoginResource, '/login')
api.add_resource(SignUpResource, '/signup')
api.add_resource(BookingResource, '/booking/<int:booking_id>', '/booking')
api.add_resource(BookingsResource, '/bookings')
app.register_blueprint(api_bp)

@app.route('/')
def index():
    form = LoginForm()

    if form.validate_on_submit():
        user = GuestService.get_guest_by_email_and_password(form.user_email.data, form.user_password.data)

        if user is None:
            return render_template('index.html', form=form, error="Unknown User")
        
        session["id_user"] = user.id_user

        return redirect(url_for("/dashboard"))

    return render_template('/templates/login.html', form=form)

@app.route('/dashboard')
def dashboard():
    # if not session["id_user"]:
    #     return redirect(url_for("/"))

    return render_template('/templates/dashboard.html')

if __name__ == '__main__':
    app.run(host="localhost", port=5001, debug=True)