from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, SelectField
from wtforms.validators import DataRequired

class UpdateBookingForm(FlaskForm):
    check_in_date = DateField('From', validators=[DataRequired()])
    check_out_date = DateField('To', validators=[DataRequired()])
    id_room = SelectField('Room Number', choices=[], validators=[DataRequired()])
    submit = SubmitField('Update')