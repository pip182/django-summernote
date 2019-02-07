# -*- coding: utf-8 -*-
"""
django_summernote.fields
~~~~~~~~~~~~~~~~~~~~~~~~

This provides django-summernote fields what can be used in forms
"""
from django.db import models
from django.forms import fields
from django_summernote.utils import using_config
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


# Original code came from https://github.com/shaunsephton/django-ckeditor
class SummernoteTextFormField(fields.CharField):
    @using_config
    def __init__(self, *args, **kwargs):
        """
        Change TextFormField widget with SummernoteWidget or SummernoteInplaceWidget.
        This follows the configuration value `iframe` to choose a proper widget.
        """
        summernote_widget = SummernoteWidget if config['iframe'] else SummernoteInplaceWidget
        kwargs.update({'widget': summernote_widget()})
        super(SummernoteTextFormField, self).__init__(*args, **kwargs)


class SummernoteTextField(models.TextField):
    def formfield(self, **kwargs):
        """
        This changes the form_class of TextField with SummernoteTextFormField
        """
        kwargs.update({'form_class': SummernoteTextFormField})
        return super(SummernoteTextField, self).formfield(**kwargs)
