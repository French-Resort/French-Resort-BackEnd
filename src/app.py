from flask import Flask, render_template, redirect, url_for, session, Blueprint
from flask_restful import Api
from models import db, Booking, Room
from forms import LoginForm, UpdateBookingForm
from services import GuestService, BookingService, RoomService, AdminService
from ressources import BookingsResource, BookingResource, DbRessource, LoginResource, SignUpResource 

app = Flask(__name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')    
api = Api(api_bp)

app.config['SECRET_KEY'] = 'YourSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/french_resort'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api.add_resource(LoginResource, '/login')
api.add_resource(SignUpResource, '/signup')
api.add_resource(BookingResource, '/booking/<int:booking_id>', '/booking')
api.add_resource(BookingsResource, '/bookings')
api.add_resource(DbRessource, '/db_init')
app.register_blueprint(api_bp)

@app.route('/', methods = ['POST', 'GET'])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        admin = AdminService.authenticate_user(form.user_email.data, form.user_password.data)

        if not admin:
            print(admin)
            return render_template('/pages/login.html', form=form, error="Invalid email or password")
        
        session["id_admin"] = admin.id_admin

        return redirect(url_for("dashboard"))

    return render_template('/pages/login.html', form=form)

@app.route('/logout', methods = ['GET'])
def logout():
    session["id_admin"] = None
    return redirect(url_for("login"))

@app.route('/dashboard', methods = ['GET'])
def dashboard():
    if not session.get("id_admin"):
        return redirect("/")

    bookings: list[Booking] = BookingService.get_all_bookings()
    total_guest_this_month = BookingService.get_total_guests_this_month()
    total_booking_this_month = BookingService.get_total_booking_this_month()
    total_earned_this_month = BookingService.get_total_earned_this_month()

    return render_template('/pages/dashboard.html', bookings=bookings, total_guest_this_month=total_guest_this_month, total_booking_this_month=total_booking_this_month, total_earned_this_month=total_earned_this_month)

@app.route('/update_booking/<int:id_booking>', methods=['GET', 'POST'])
def update_booking(id_booking):
    if not session.get("id_admin"):
        return redirect(url_for("/"))

    booking: Booking = BookingService.get_booking_by_id(id_booking)

    if not booking:
        return redirect(url_for("dashboard"))

    rooms: list[Room] = RoomService.get_all_rooms()

    form = UpdateBookingForm()
    form.room_type.choices = [room.room_type for room in rooms]

    if form.validate_on_submit():
        room: Room = RoomService.get_room_by_id(form.room_type.data)

        if not room:
            return render_template('update_booking.html', form=form, booking=booking)

        BookingService.update_booking(id_booking, form.booking_check_in_date.data, form.booking_check_out_date.data, booking.id_guest, room.id_room)

    return render_template('update_booking.html', form=form, booking=booking)

@app.route('/delete_booking/<int:id_booking>', methods=['GET'])
def delete_booking(id_booking):
    if session.get("id_admin"):
        return redirect("/")
    
    try:
        BookingService.delete_booking(id_booking)
        return redirect(url_for("dashboard"))
    except ValueError as v:
        return redirect(url_for("update", id_booking=id_booking))

if __name__ == '__main__':
    app.run(host="localhost", port=5001, debug=True)