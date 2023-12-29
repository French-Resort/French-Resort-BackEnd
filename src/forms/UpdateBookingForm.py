from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, SelectField
from wtforms.validators import DataRequired

class UpdateBookingForm(FlaskForm):
    check_in_date = DateField('Check in date', validators=[DataRequired()])
    check_out_date = DateField('Check out date', validators=[DataRequired()])
    id_room = SelectField('Room Number', choices=[], validators=[DataRequired()])
    submit = SubmitField('Update')