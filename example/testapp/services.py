from django.contrib.auth import get_user_model


def create_user_account(email, password, first_name="", last_name="", **other_fields):
    user = get_user_model().objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        **other_fields,
    )
    return user


def get_user_by_email(email: str):
    return get_user_model().objects.filter(email__iexact=email).first()
