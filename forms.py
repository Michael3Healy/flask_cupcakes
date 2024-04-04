from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField
from wtforms.validators import InputRequired, Optional, URL

class AddCupcakeForm(FlaskForm):
    '''Form for adding cupcake'''

    flavor = StringField('Flavor', validators=[InputRequired()])
    size = SelectField('Size', choices=[('small', 'Small'), ('large', 'Large')])
    rating = FloatField('Rating', validators=[InputRequired()])
    image = StringField('Image URL', validators=[URL(), Optional()])