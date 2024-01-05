from flask_wtf import FlaskForm
from wtforms import SubmitField, DecimalField, StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class UpdateOrCreateRoomForm(FlaskForm):
    id_room = StringField('Room Number', validators=[DataRequired()])
    room_type = StringField('Room Type', validators=[DataRequired()])
    price_per_night = DecimalField('Price per night', validators=[DataRequired(), NumberRange(100.0, 50000.0)])
    max_guests = IntegerField('Max guests', validators=[DataRequired(), NumberRange(1, 10)])
    submit = SubmitField('Send')