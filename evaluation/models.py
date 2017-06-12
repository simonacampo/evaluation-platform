# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from urllib import parse as urlparse
import uuid

from adminsortable.models import SortableMixin
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.crypto import get_random_string
from enumfields import Enum, EnumField


class Gender(Enum):
    MALE = "m"
    FEMALE = "f"
    OTHER = "o"


@python_2_unicode_compatible
class Evaluator(models.Model):
    """"Someone who evaluates a platform"""
    user = models.OneToOneField("auth.User", on_delete=models.SET_NULL, null=True,
                                blank=True, related_name="evaluator")
    email = models.EmailField(null=True, blank=True)

    birth_date = models.DateField(null=False)
    gender = EnumField(Gender, null=False, max_length=1)

    @property
    def identifier(self):
        eval_identifier = self.email or "evaluator_%s" % self.id

        if self.user:
            eval_identifier = self.evaluator.user.get_username()

        return eval_identifier

    def __str__(self):
        parts = []

        email = self.email

        if self.user:
            email = self.user.email
            parts.append(self.user.get_username())

        if email:
            parts.append(email)

        parts.append(str(self.id))

        return " ".join(parts)


@python_2_unicode_compatible
class Platform(models.Model):
    """An online platform to be evaluated"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    url = models.URLField(help_text="This is the link that people evaluating the platform will go to")

    def __str__(self):
        domain = urlparse.urlparse(self.url).netloc
        return "%s (%s)" % (self.name, domain)


HEURISTIC_CATEGORIES = {
    "m": "Members",
    "p": "Platform",
    "M": "Moderation",
    "c": "Common Ground",
    "C": "Contribution",
    "P": "Purpose"
}


@python_2_unicode_compatible
class Heuristic(models.Model):
    """A heuristic, measured by answers to questions"""
    name = models.CharField(max_length=200)
    category_code = models.CharField(max_length=20, choices=HEURISTIC_CATEGORIES.items())

    @property
    def category(self):
        return HEURISTIC_CATEGORIES[self.category_code]

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Question(SortableMixin):
    """A question to ask people when evaluating a platform"""

    class Meta:
        ordering = ["question_order"]

    question_order = models.SmallIntegerField(editable=False, db_index=True, default=0)

    platform = models.ForeignKey(Platform, related_name="questions")
    heuristic = models.ForeignKey(Heuristic, related_name="questions")

    question = models.TextField()
    explanation = models.TextField(blank=True, help_text="To help clarify how to answer the question")

    def __str__(self):
        return self.question


def code_generator():
    return get_random_string(length=6)


@python_2_unicode_compatible
class Evaluation(models.Model):
    """An evaluation of a platform, performed by an Evaluator"""
    evaluator = models.ForeignKey(Evaluator, on_delete=models.CASCADE,
                                  related_name="evaluations")
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE,
                                 related_name="evaluations")
    started = models.DateTimeField()
    first_continue = models.DateTimeField()

    verification_code = models.CharField(db_index=True, default=code_generator, max_length=6)

    def __str__(self):
        return "%s's evaluation of %s" % (self.evaluator.identifier, self.platform.name)


@python_2_unicode_compatible
class Answer(models.Model):
    """An answer to an evaluation question"""
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE,
                                   related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name="answers")

    score = models.SmallIntegerField()
    explanation = models.TextField(blank=True)
    screen_shot = models.URLField(blank=True, null=True)
    answer_time = models.DateTimeField()

    def __str__(self):
        return "Answer to question %s in %s" % (self.question.id, self.evaluation)
