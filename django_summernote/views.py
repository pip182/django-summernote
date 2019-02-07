# -*- coding: utf-8 -*-
"""
django_summernote.views
~~~~~~~~~~~~~~~~~~~~~~~

This file includes django-summernote views
"""
from django import VERSION as django_version
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from django_summernote.utils import get_attachment_model, using_config
try:
    # Django >= 1.10
    from django.views import View
except ImportError:
    from django.views.generic import View


class SummernoteEditor(TemplateView):
    """SummernoteEditor provides a view for iframe-ed editor"""
    template_name = 'django_summernote/widget_iframe_editor.html'

    @using_config
    def __init__(self):
        super(SummernoteEditor, self).__init__()

        # Create css and js files by merging default files and given by user.
        static_default_css = tuple(static(x) for x in config['default_css'])
        static_default_js = tuple(static(x) for x in config['default_js'])

        self.css = \
            config['base_css'] \
            + (config['codemirror_css'] if 'codemirror' in config else ()) \
            + static_default_css \
            + config['css']

        self.js = \
            config['base_js'] \
            + (config['codemirror_js'] if 'codemirror' in config else ()) \
            + static_default_js \
            + config['js']

    @using_config
    def get_context_data(self, **kwargs):
        # Pass variables for template rendering
        context = super(SummernoteEditor, self).get_context_data(**kwargs)

        # Id of original element (e.g. textarea)
        context['id_src'] = self.kwargs['id']

        # Replace dash with underscore to prevent errors
        context['id'] = self.kwargs['id'].replace('-', '_')
        
        # Pass generated variables to renderer
        context['css'] = self.css
        context['js'] = self.js
        context['config'] = config

        return context


class SummernoteUploadAttachment(View):
    """SummernoteUploadAttachment stores files as configured attachment model"""
    def __init__(self):
        super(SummernoteUploadAttachment, self).__init__()

    def get(self, request, *args, **kwargs):
        """GET requests are not allowed"""
        return JsonResponse({
            'status': 'false',
            'message': _('Only POST method is allowed'),
        }, status=400)

    @using_config
    def post(self, request, *args, **kwargs):
        """Store files when user requests as POST method"""

        # Check whether user was authenticated or not
        authenticated = \
            request.user.is_authenticated if django_version >= (1, 10) \
            else request.user.is_authenticated()

        # Only authenticated users are allowed to upload if the option is True
        if config['attachment_require_authentication'] and \
                not authenticated:
            return JsonResponse({
                'status': 'false',
                'message': _('Only authenticated users are allowed'),
            }, status=403)

        # Find files in the request
        if not request.FILES.getlist('files'):
            return JsonResponse({
                'status': 'false',
                'message': _('No files were requested'),
            }, status=400)

        # Remove unnecessary CSRF token, if found
        kwargs = request.POST.copy()
        kwargs.pop("csrfmiddlewaretoken", None)

        try:
            attachments = []

            for file in request.FILES.getlist('files'):

                # Create instance of appropriate attachment class
                klass = get_attachment_model()
                attachment = klass()

                attachment.file = file
                attachment.name = file.name

                if file.size > config['attachment_filesize_limit']:
                    return JsonResponse({
                        'status': 'false',
                        'message': _('File size exceeds the limit allowed and cannot be saved'),
                    }, status=400)

                # Calling save method with attachment parameters as kwargs
                attachment.save(**kwargs)
                attachments.append(attachment)

            return HttpResponse(render_to_string('django_summernote/upload_attachment.json', {
                'attachments': attachments,
            }), content_type='application/json')
        except IOError:
            return JsonResponse({
                'status': 'false',
                'message': _('Failed to save attachment'),
            }, status=500)
