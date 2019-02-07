# -*- coding: utf-8 -*-
"""
django_summernote.apps
~~~~~~~~~~~~~~~~~~~~~~

App class for django_summernote which holds app configuration
"""
from django.apps import AppConfig
from django.conf import settings as django_settings
from django_summernote.utils import (
    LANG_TO_LOCALE, uploaded_filepath, get_theme_files
)


class DjangoSummernoteConfig(AppConfig):
    name = 'django_summernote'
    verbose_name = 'Django Summernote'

    # Default theme is Bootstrap 3
    theme = 'bs3'

    # Actual configuration
    config = {}

    def __init__(self, app_name, app_module):
        super(DjangoSummernoteConfig, self).__init__(app_name, app_module)
        self.update_config()

    def get_default_config(self):
        """Return default configuration values"""
        return {
            # Using SummernoteWidget(iframe widget) for admin pages by default
            'iframe': True,

            # These strings will be assumed as empty.
            'empty': ('<p><br/></p>', '<p><br></p>'),

            # Language-to-locale conversion table
            'lang_matches': LANG_TO_LOCALE,

            # Attachment settings
            'disable_attachment': False,
            'attachment_upload_to': uploaded_filepath,
            'attachment_storage_class': None,
            'attachment_filesize_limit': 1024 * 1024,
            'attachment_require_authentication': False,
            'attachment_model': 'django_summernote.Attachment',

            # Shortcut name for jQuery
            'jquery': '$',

            # Base media files only for SummernoteWidget
            'base_css': '',
            'base_js': '',

            # Media files for CodeMirror
            'codemirror_css': (
                '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.40.0/codemirror.min.css',
            ),
            'codemirror_js': (
                '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.40.0/codemirror.js',
                '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.40.0/mode/xml/xml.js',
                '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.40.0/mode/htmlmixed/htmlmixed.js',
            ),

            # Media files for all Summernote widgets
            'default_css': '',
            'default_js': '',

            # Additional media files only for SummernoteWidget
            'css': (),
            'js': (),

            # Additional media files only for SummernoteInplacewidget
            'css_for_inplace': (),
            'js_for_inplace': (),

            # For lazy loading (inplace widget only)
            'lazy': False,

            # Summernote settings
            'summernote': {
                'width': 720,
                'height': 480,
                'lang': None,
                'toolbar': [
                    ['style', ['style']],
                    ['font', ['bold', 'italic', 'underline', 'superscript', 'subscript',
                              'strikethrough', 'clear']],
                    ['fontname', ['fontname']],
                    ['fontsize', ['fontsize']],
                    ['color', ['color']],
                    ['para', ['ul', 'ol', 'paragraph']],
                    ['height', ['height']],
                    ['table', ['table']],
                    ['insert', ['link', 'picture', 'video', 'hr']],
                    ['view', ['fullscreen', 'codeview']],
                    ['help', ['help']],
                ],
            }
        }

    def _copy_old_configs(self, user, default):
        """
        NOTE: Will be deprecated from 0.9

        Copy old-style configurations for backword-compatibility.
        """
        DEPRECATED_SUMMERNOTE_CONFIGS = (
            'width',
            'height',
            'lang',
            'toolbar',
        )
        for key in DEPRECATED_SUMMERNOTE_CONFIGS:
            if user.get(key):
                self.config['summernote'][key] = user.get(key)
            if not self.config['summernote'].get(key):
                self.config['summernote'][key] = default['summernote'].get(key)

    def update_config(self):
        """
        Merge configuration dictionaries.

        self.config is an actual configuration dictionary that will be used in running.
        This function create self.config by merging default configuration dict with 
        given `SUMMERNOTE_CONFIG`. And it also update self.config by setting theme files.
        """
        self.theme = getattr(django_settings, 'SUMMERNOTE_THEME', 'bs3')
        DEFAULT_CONFIG = self.get_default_config()

        CONFIG = getattr(django_settings, 'SUMMERNOTE_CONFIG', {})
        for key in ('base_css', 'base_js', 'default_css', 'default_js'):
            CONFIG[key] = get_theme_files(self.theme, key)

        self.config = DEFAULT_CONFIG.copy()
        self.config.update(CONFIG)
        self._copy_old_configs(CONFIG, DEFAULT_CONFIG)

    def ready(self):
        pass
