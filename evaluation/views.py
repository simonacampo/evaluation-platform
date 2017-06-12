# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict

import arrow
from django.shortcuts import redirect, render
from formtools.wizard.views import CookieWizardView

from evaluation.models import Platform, Evaluation, Answer
from evaluation.forms import StartForm, DemographicsForm, AnswerForm, EmailForm


class EvaluationWizardView(CookieWizardView):
    platform = None

    @property
    def question(self):
        if self.steps.current.startswith("q_"):
            i = self.steps.current.split("_")[1]
            return self.platform.questions.all()[int(i)]

    def __init__(self, platform, **kwargs):
        super(EvaluationWizardView, self).__init__(**kwargs)
        self.platform = platform

    def get_template_names(self):
       if self.steps.current == "start":
           return "evaluation/start.html"

       if self.steps.current == "demographics":
           return "evaluation/demographics.html"

       if self.steps.current == "email":
           return "evaluation/end.html"

       if self.steps.current.startswith("q_"):
           return "evaluation/question.html"

       raise ValueError("Unkown step: %s" % self.steps.current)

    def get_context_data(self, form, **kwargs):
        context = super(EvaluationWizardView, self).get_context_data(form, **kwargs)
        context.update({
            "title": "Evaluate %s" % (self.platform.name),
            "platform": self.platform,
            "question": self.question
        })

        return context

    def process_step(self, form):
        data = dict(self.get_form_step_data(form))

        if self.steps.current == "start":
            data["first_open"] = self.request.session.get(
                "platform_first_view_%s" % self.platform.id, arrow.utcnow().timestamp)

        data["answered"] = arrow.utcnow().timestamp

        return data

    def done(self, forms_list, form_dict=None, **kwargs):
        evaluation = self.create_evaluation(form_dict)
        return redirect("evaluation:finished",
                        platform_id=str(self.platform.id),
                        evaluation_id=str(evaluation.id),
                        evaluation_code = evaluation.verification_code
                        )

    def create_evaluation(self, form_dict):
        evaluator = form_dict["demographics"].save(commit=False)
        evaluator.email = form_dict["email"].cleaned_data.get("email", None)
        evaluator.save()

        started = arrow.get(dict(self.storage.get_step_data("start"))["first_open"])
        first_continue = arrow.get(dict(self.storage.get_step_data("start"))["answered"])
        evaluation = Evaluation(
            platform=self.platform,
            evaluator=evaluator,
            started=started.datetime,
            first_continue=first_continue.datetime
        )

        evaluation .save()

        for i, question in enumerate(self.platform.questions.all()):
            step = "q_%s" % i
            answer = form_dict[step].save(commit=False)
            answer.evaluation = evaluation
            answer.question = question
            answer.answer_time = arrow.get(dict(self.storage.get_step_data(step))["answered"]).datetime
            answer.save()



        return evaluation


def evaluation_wizard_view_wrapper(request, *args, **kwargs):
    # Normally, FormWizard takes its forms list as a kwarg to as_view(), or as
    # a class attribute. In both cases, the list would need to be set up when
    # the view is defined, not when it is executed. But we need to generate this
    # list dynamicly based on the number of questions, so we're wrapping the view to do that.
    platform = Platform.objects.get(pk=kwargs.get("platform_id"))

    request.session.setdefault("platform_first_view_%s" % platform.id, arrow.utcnow().timestamp)

    forms = OrderedDict()
    forms["start"] = StartForm
    forms["demographics"] = DemographicsForm

    for i in range(platform.questions.count()):
        forms["q_%s" % i] = AnswerForm

    forms["email"] = EmailForm

    view = EvaluationWizardView.as_view(form_list=forms.items(), platform=platform)
    return view(request, *args, **kwargs)


def evaluation_finished(request, *args, **kwargs):
    if not Evaluation.objects.filter(
        pk=kwargs.get("evaluation_id"),
        verification_code=kwargs.get("evaluation_code"),
        platform_id=kwargs.get("platform_id")
    ).exists():
        raise Evaluation.DoesNotExist


    return render(request, "evaluation/finished.html", {
        "title": "Thank you!",
        "verification_code": kwargs.get("evaluation_code")
    })
