# accounts/middleware.py
from django.utils.cache import add_never_cache_headers


class DisableClientSideCachingMiddleware:
    """
    Prevents browsers from caching sensitive pages when a user is authenticated.
    Fixes the issue of seeing protected data by clicking 'Back' after logout.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if hasattr(request, "user") and request.user.is_authenticated:
            add_never_cache_headers(response)
        return response
