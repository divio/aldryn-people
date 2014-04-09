from django.conf import settings


def get_additional_styles():
    """
    Get additional styles choices from settings
    """
    styles = getattr(settings, 'PEOPLE_PLUGIN_STYLES', '')
    choices = [(style.strip().lower(), style.title()) for style in styles.split(',')]
    return choices
