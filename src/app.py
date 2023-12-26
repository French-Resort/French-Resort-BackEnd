from models import db
from forms import LoginForm, UpdateForm
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YourSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/french_resort'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    form = LoginForm()

    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)