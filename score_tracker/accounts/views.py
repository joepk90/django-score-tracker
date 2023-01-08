from djoser.views import UserViewSet

class CustomDjsoserUserViewSet(UserViewSet):
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
        'head',
        'options',
    ]
