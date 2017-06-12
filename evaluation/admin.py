# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from django.forms import widgets
from django.shortcuts import resolve_url
from django.utils.text import mark_safe
from adminsortable.admin import NonSortableParentAdmin, SortableTabularInline

# Register your models here.

from evaluation.models import Platform, Question, Heuristic, Evaluator,\
    Evaluation, Answer


class EvaluatorAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "email")
    readonly_fields = ("id",)


class QuestionInline(SortableTabularInline):
    model = Question
    extra = 1

    formfield_overrides = {
        models.TextField: {'widget': widgets.Textarea(attrs={'rows': 2, 'cols': 40})},
    }


class PlatformAdmin(NonSortableParentAdmin):
    list_display = ("name", "url", "evaluation_url")
    inlines = (QuestionInline, )
    readonly_fields = ("evaluation_link",)

    def sort_view(self, request):
        self.request = request
        return super(PlatformAdmin, self).sort_view(request)

    def changelist_view(self, request, extra_context=None):
        self.request = request
        return super(PlatformAdmin, self).changelist_view(request)

    def change_view(self, request, *args, **kwargs):
        self.request = request
        return super(PlatformAdmin, self).change_view(request, *args, **kwargs)

    def evaluation_url(self, platform):
        if not platform.id:
            return None
        return self.request.build_absolute_uri(
            resolve_url("evaluation:evaluation", platform_id=platform.id)
        )

    def evaluation_link(self, platform):
        url = self.evaluation_url(platform)
        if not url:
            return "This will be generated as soon as you save the platform."
        return '<a href="%s" target="_blank">%s</a>' % (url, url)

    evaluation_link.allow_tags = True


class HeuristicAdmin(admin.ModelAdmin):
    list_display = ("name", "category")


class AnswerInline(admin.TabularInline):
    model = Answer


class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("evaluator", "platform", 'verification_code')
    inlines = (AnswerInline, )
    readonly_fields = ("verification_code", )


admin.site.register(Platform, PlatformAdmin)
admin.site.register(Heuristic, HeuristicAdmin)
admin.site.register(Evaluator, EvaluatorAdmin)
admin.site.register(Evaluation, EvaluationAdmin)