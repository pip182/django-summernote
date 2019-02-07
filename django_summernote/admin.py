# -*- coding: utf-8 -*-
"""
django_summernote.admin
~~~~~~~~~~~~~~~~~~~~~~~

This module include helpers for using Summernote widgets in Django Admin
"""
from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.db import models
from django_summernote.utils import get_attachment_model, using_config
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class SummernoteModelAdminMixin(object):
    """This mixin changes the widget of TextField with Summernote."""

    # This checks entire fields by default.
    summernote_fields = '__all__'

    @using_config
    def formfield_for_dbfield(self, db_field, *args, **kwargs):
        """
        Change the widget of TextField with SummernoteWidget or SummernoteInplaceWidget.
        This follows the configuration value `iframe` to choose a proper widget.
        """
        summernote_widget = SummernoteWidget if config['iframe'] else SummernoteInplaceWidget

        # If we have to check whole fields,
        if self.summernote_fields == '__all__':
            if isinstance(db_field, models.TextField):
                kwargs['widget'] = summernote_widget
        # Or, within given fields.
        else:
            if db_field.name in self.summernote_fields:
                kwargs['widget'] = summernote_widget

        return super(SummernoteModelAdminMixin, self).formfield_for_dbfield(db_field, *args, **kwargs)


class SummernoteInlineModelAdmin(SummernoteModelAdminMixin, InlineModelAdmin):
    """As a shortcut for InlineModelAdmin."""
    pass


class SummernoteModelAdmin(SummernoteModelAdminMixin, admin.ModelAdmin):
    """As a shortcut for default ModelAdmin."""
    pass


class AttachmentAdmin(admin.ModelAdmin):
    """Admin class for default attachment model."""

    list_display = ['name', 'file', 'uploaded']
    search_fields = ['name']
    ordering = ('-id',)

    def save_model(self, request, obj, form, change):
        # Assing a name along to the filename when no name was given.
        obj.name = obj.file.name if (not obj.name) else obj.name
        super(AttachmentAdmin, self).save_model(request, obj, form, change)


admin.site.register(get_attachment_model(), AttachmentAdmin)
