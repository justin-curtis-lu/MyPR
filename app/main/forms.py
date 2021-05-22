from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User
from markupsafe import Markup
from flask_wtf.file import FileField, FileRequired, FileAllowed


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class PostForm(FlaskForm):
    title = TextAreaField('Title', validators=[
        DataRequired(), Length(min=1, max=30)])
    post = TextAreaField('Description', validators=[
        DataRequired(), Length(min=1, max=700)])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'mp4'], 'Images (jpg/png) or Videos (mp4) only!')])
    submit = SubmitField('Publish')
