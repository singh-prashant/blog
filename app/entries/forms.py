from wtforms import Form, StringField, TextAreaField,SelectField
from wtforms.validators import DataRequired
from models import Entry

class EntryForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    status = SelectField(
        'Entry Status',
        choices=(
            (Entry.STATUS_PUBLIC,'Public'),
            (Entry.STATUS_DRAFT,'Draft')),
        coerce=int
    )
    def save_entry(self, entry):
        self.populate_obj(entry)
        entry.generate_slug()
        return entry