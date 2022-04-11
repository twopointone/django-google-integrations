# Third Party Stuff
from rest_framework import serializers

# Django Google Integrations Stuff
from django_google_integrations.models import GoogleAuthIntermediateState


class GoogleAuthSerializer(serializers.Serializer):
    state = serializers.CharField()
    auth_code = serializers.CharField()
    code_verifier = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(GoogleAuthSerializer, self).__init__(*args, **kwargs)
        self._code_verifier = ""

    def validate_state(self, value):
        intermediate_state_obj = GoogleAuthIntermediateState.objects.filter(
            state=value
        ).first()

        if not intermediate_state_obj:
            raise serializers.ValidationError(
                "No auth-state %s exists for the user" % value
            )

        # Defined here to save a db-call
        self._code_verifier = intermediate_state_obj.code_verifier

        return value

    def get_code_verifier(self, data):
        return self._code_verifier


class IOSGoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField()
