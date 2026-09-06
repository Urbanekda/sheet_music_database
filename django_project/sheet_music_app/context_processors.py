from django.conf import settings


def turnstile(request):
    """Expose the Turnstile site key (public, safe to embed) to all templates."""
    return {"TURNSTILE_SITE_KEY": settings.TURNSTILE_SITE_KEY}
