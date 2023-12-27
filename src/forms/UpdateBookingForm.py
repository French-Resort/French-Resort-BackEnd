from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, SelectField, DecimalField, IntegerField
from wtforms.validators import DataRequired, NumberRange, ReadOnly

class UpdateBookingForm(FlaskForm):
    check_in_date = DateField('From', validators=[DataRequired()])
    check_out_date = DateField('From', validators=[DataRequired()])
    room_type = SelectField('Room Type', choices=[], validators=[DataRequired()])
    total_price = DecimalField('Total price', validators=[DataRequired(), NumberRange(0, 1000000000000)])
    submit = SubmitField('Log In')