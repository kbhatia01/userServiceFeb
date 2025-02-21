from Customuser.models import User


def sign_up_service(email, password, username):
    u = User(email=email, name=username, username=email)
    u.set_password(password)
    u.save()
    return u


def login_service(email, password):
    try:
        u = User.objects.get(email=email)
        if u.check_password(password):
            return u.generate_auth_token(), None

        return None, Exception('Incorrect email or password')
    except User.DoesNotExist:
        return None, Exception('User does not exist')
