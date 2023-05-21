from rest_framework import authentication
from rest_framework import exceptions


from webdav.services import AuthenticationService


class AppAuthentication(authentication.BaseAuthentication):
    authentication = AuthenticationService()

    def authenticate(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            raise exceptions.AuthenticationFailed("Unauthorized.")

        authenticated_token = self.authentication.authenticated_token(token=token)

        return (authenticated_token.user, None)
