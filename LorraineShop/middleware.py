from django.utils import translation


class ForceAdminLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith("/static/") or request.path.startswith("/media/"):
            return self.get_response(request)

        # 👉 Admin isolé
        if request.path.startswith("/admin-fr/"):
            translation.activate("fr")
            request.LANGUAGE_CODE = "fr"

        return self.get_response(request)
