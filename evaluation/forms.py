import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import MultiWidgetField
from crispy_forms.bootstrap import InlineRadios
from django.forms import ModelForm, Form, BooleanField, EmailField, ChoiceField
from django.forms import widgets

from evaluation.models import Answer, Evaluator


class DateInput(widgets.DateInput):
    input_type = 'date'


SCORE_CHOICES = [
    (0, "Strongly Disagree"),
    (1, "Disagree"),
    (2, "Neutral"),
    (3, "Agree"),
    (4, "Strongly Agree"),
    (-1, "Unable to Answer")
]

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ["score", "explanation", "screen_shot"]
        widgets = {
            "score": widgets.RadioSelect
        }
        help_texts = {
            'explanation': 'Please explain your choice with your findings',
            'screen_shot': 'Support your explanation with a screenshot link using <a href="https://snag.gy/" target="_blank">Snag.gy</a>. Copy the generated url into the field',
        }

    score = ChoiceField(choices=SCORE_CHOICES)

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.add_layout(InlineRadios("score"))



checkbox_label = "I declare to have visited and explored the platform for around 5 minutes"
class StartForm(Form):
    check = BooleanField(required=True, label=checkbox_label)


this_year = datetime.datetime.today().year
class DemographicsForm(ModelForm):
    class Meta:
        model = Evaluator
        fields = ["birth_date", "gender"]
        widgets = {
            "birth_date": widgets.SelectDateWidget(
                years=range(this_year, this_year - 100, -1)
            )
        }

    gender = ChoiceField(
        choices=Evaluator._meta.get_field("gender").choices,
        widget=widgets.RadioSelect
    )

    def __init__(self, *args, **kwargs):
        super(DemographicsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.add_layout(
            MultiWidgetField('birth_date',
                             attrs=({
                                 'style': 'width: 33%; display: inline-block;max-width:100px;'
                             }))
        )

email_help_text = """(Optional) click the "continue" button to finish receive the code for Microworkers
"""
class EmailForm(Form):
    email = EmailField(required=False, label="E-mail", help_text=email_help_text)

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
