from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, SelectField
from wtforms.validators import DataRequired

class UpdateBookingForm(FlaskForm):
    booking_check_in_date = DateField('From', validators=[DataRequired()])
    booking_check_out_date = DateField('From', validators=[DataRequired()])
    room_type = SelectField('Room Type', choices=[], validators=[DataRequired()])
    submit = SubmitField('Log In')