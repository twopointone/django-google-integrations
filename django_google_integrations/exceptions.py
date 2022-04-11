# Third Party Stuff
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, status


class GoogleException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Google Operational error")


class GoogleAuthException(GoogleException):
    default_detail = _("Google auth error")
