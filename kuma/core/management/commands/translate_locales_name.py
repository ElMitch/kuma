from django.conf import settings
from django.core.management.base import BaseCommand


# A script to generate a template which will be used to localize the supported locale name
# For more inofrmation see https://bugzil.la/859499#c11

class Command(BaseCommand):
    help = "Generate a template to get the locales name localized"

    def handle(self, *args, **options):
        template_string = (u"This template is automatically generated by"
                           "scripts/translate_locales.py to make the"
                           "languages name localizable."
                           "Do not edit it manually\n"
                           "Background: https://bugzil.la/859499#c11\n")

        LANGUAGES = sorted([lang_info.english
                            for lang_code, lang_info in settings.LOCALES.items()
                            if lang_code in settings.MDN_LANGUAGES])

        for lang in LANGUAGES:
            template_string += "{{ _('%s') }}\n" % lang

        jinja_path = settings.TEMPLATES[0]["DIRS"][0]
        template_path = jinja_path + '/includes/translate_locales.html'

        outfile = open(template_path, "w")
        outfile.write(template_string)
        outfile.close()
