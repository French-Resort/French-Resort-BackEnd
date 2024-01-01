import requests
import os
from flask import Flask, render_template, redirect, url_for, session, Blueprint, request
from flask_cors import CORS
from flask_restful import Api
from models import db, Booking, Room
from forms import LoginForm, UpdateBookingForm
from services import BookingService, RoomService, AdminService
from resources import *


app = Flask(__name__)
CORS(app)
api_bp = Blueprint('api', __name__, url_prefix='/api')    
api = Api(api_bp)

app.config['SECRET_KEY'] = 'YourSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv("POSTGRES_USER", default="postgres")}:{os.getenv("POSTGRES_PASSWORD", default="postgres")}@{os.getenv("POSTGRES_HOST", default="localhost")}/french_resort'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api.add_resource(LoginResource, '/login', endpoint='login')
api.add_resource(SignUpResource, '/signup', endpoint='signup')
api.add_resource(BookingResource, '/booking', endpoint='booking')
api.add_resource(BookingByIdResource, '/booking/<int:id_booking>', endpoint='booking_by_id')
api.add_resource(BookingsResource, '/bookings', endpoint='bookings')
api.add_resource(BookingsByIdGuest, '/bookings/<int:id_guest>', endpoint='bookings_by_id_guest')
api.add_resource(RoomResource, '/room', endpoint='room')
api.add_resource(RoomsResource, '/rooms', endpoint='rooms')
api.add_resource(RoomsAvailableResource, '/rooms/available', endpoint='rooms_available')
api.add_resource(DbResource, '/db_init', endpoint='db_init')
app.register_blueprint(api_bp)

@app.route('/', methods = ['POST', 'GET'])
def index():
    if session.get("id_admin"):
        return redirect(url_for("dashboard"))
    
    form = LoginForm()

    if form.validate_on_submit():
        admin = AdminService.authenticate_user(form.user_email.data, form.user_password.data)

        if not admin:
            return render_template('/pages/login.html', form=form, error="Invalid email or password")
        
        session["id_admin"] = admin.id_admin

        return redirect(url_for("dashboard"))

    return render_template('/pages/login.html', form=form)

@app.route('/logout', methods = ['GET'])
def logout():
    session["id_admin"] = None
    return redirect("/")

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
    
    current_room: Room = RoomService.get_room_by_id(booking.id_room)

    if request.method == "POST" :
        form = UpdateBookingForm(request.form)
        rooms: list[Room] = RoomService.get_all_rooms_available_from_to_date(form.check_in_date.data.strftime('%Y-%m-%d'), form.check_out_date.data.strftime('%Y-%m-%d'))
        
        if current_room not in rooms: 
            rooms.append(current_room)

        form.id_room.choices = [(room.id_room, f'{room.id_room} - {room.room_type}') for room in rooms]
    else:
        form = UpdateBookingForm()
        form.check_in_date.data = booking.check_in_date
        form.check_out_date.data = booking.check_out_date
        form.id_room.data = booking.id_room
        
        rooms: list[Room] = RoomService.get_all_rooms_available_from_to_date(booking.check_in_date, booking.check_out_date)
        if current_room not in rooms: 
            rooms.append(current_room)
        
        form.id_room.choices = [(room.id_room, f'{room.id_room} - {room.room_type}') for room in rooms]

    if form.validate_on_submit(): 
        try:
            booking: Booking = BookingService.update_booking(booking.id_booking, form.check_in_date.data.strftime('%Y-%m-%d'), form.check_out_date.data.strftime('%Y-%m-%d'), booking.id_guest, form.id_room.data)
            return redirect(url_for("dashboard"))
        except Exception as e:
            return render_template('pages/updateBooking.html', form=form, booking=booking, error=e.__str__())

    return render_template('pages/updateBooking.html', form=form, booking=booking)

def bdd_init():
    url = "http://localhost:5001/api/db_init"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        result = response.json()
        print(result)

    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")

if __name__ == '__main__':
    app.run(host="localhost", port=os.getenv("PORT", default=5001), debug=True)