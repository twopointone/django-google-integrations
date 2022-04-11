# Third Party Stuff
from rest_framework import serializers
from testapp.models import User


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "google_id", "date_joined"]
