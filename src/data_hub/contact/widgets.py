from django.forms.widgets import Widget
from django.template import loader
from django.utils.safestring import mark_safe
import logging, watchtower

logger = logging.getLogger("errLog")
logger.addHandler(watchtower.CloudWatchLogHandler())

class ProtectedFileWidget(Widget):
    template_name = 'protected_widget.html'

    def get_context(self, name, value, attrs=None):
        try:
            return {'widget': {
                'name': name,
                'value': value,
            }}
        except Exception as e:
            logger.error(str(e))

    def render(self, name, value, attrs=None, renderer=None):
        try:
            context = self.get_context(name, value, attrs)
            template = loader.get_template(self.template_name).render(context)
            return mark_safe(template)
        except Exception as e:
            logger.error(str(e))