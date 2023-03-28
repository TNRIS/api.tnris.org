from django.forms.widgets import Widget
from django.template import loader
from django.utils.safestring import mark_safe
import logging, watchtower

logger = logging.getLogger("errLog")
logger.addHandler(watchtower.CloudWatchLogHandler())

class ProtectedFileWidget(Widget):
    template_name = 'protected_widget.html'

    def get_context(self, name, value, attrs=None):
        logger.info("Getting to get_context")
        try:
            return {'widget': {
                'name': name,
                'value': value,
            }}
        except Exception as e:
            logger.error(str(e))

    def render(self, name, value, attrs=None, renderer=None):
        logger.info("Getting to render")
        try:
            logger.info("Getting context")
            context = self.get_context(name, value, attrs)
            logger.info("Loading template")
            template = loader.get_template(self.template_name).render(context)
            logger.info("Marking safe.")
            return mark_safe(template)
        except Exception as e:
            logger.error(str(e))