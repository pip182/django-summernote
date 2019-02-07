# -*- coding: utf-8 -*-
"""
django_summernote.urls
~~~~~~~~~~~~~~~~~~~~~~

This module contains URLs of django-summernote
"""
from django.conf.urls import url

from django_summernote.views import (
    SummernoteEditor, SummernoteUploadAttachment
)

urlpatterns = [
    # for SummernoteWidget (will be rendered in iframe)
    url(r'^editor/(?P<id>.+)/$', SummernoteEditor.as_view(),
        name='django_summernote-editor'),
    # for uploading attachment
    url(r'^upload_attachment/$', SummernoteUploadAttachment.as_view(),
        name='django_summernote-upload_attachment'),
]
