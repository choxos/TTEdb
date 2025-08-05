"""
Context processors for TTEdb project.
"""
from django.conf import settings

def settings(request):
    """
    Make certain settings available in templates.
    """
    return {
        'settings': {
            'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
            'ENABLE_ANALYTICS': settings.ENABLE_ANALYTICS,
            'DEBUG': settings.DEBUG,
        }
    } 