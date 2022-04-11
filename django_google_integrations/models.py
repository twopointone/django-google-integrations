# Standard Library
import uuid

# Third Party Stuff
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class GoogleAuthIntermediateState(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    state = models.CharField(max_length=64, unique=True)
    code_verifier = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = _("Google Auth Intermediate State")
        verbose_name_plural = _("Google Auth Intermediate States")
        ordering = ("-created_at",)


class UserGoogleAuthCredential(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = _("User Google Auth Credential")
        verbose_name_plural = _("User Google Auth Credentials")
        ordering = ("-created_at",)

    @property
    def is_expired(self):
        return self.expires_at < timezone.now()
