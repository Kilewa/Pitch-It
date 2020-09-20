from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,ValidationError
from wtforms.validators import Required,Email
from ..models import User,Comment,Pitch

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')


class PitchForm(FlaskForm):
    title=StringField('Pitch title',validators=[Required()])
    pitch=TextAreaField('Pitch description.',validators = [Required()])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    comment=TextAreaField('Pitch comment.',validators = [Required()])
    submit = SubmitField('Submit')