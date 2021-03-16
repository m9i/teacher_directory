"""
Handling permissions for users who are assigned 
for basic level actions in the project. (view few data, modify some of their data etc).

"""
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def permission_error(request):
    return HttpResponse('You don\'t have right permissio to access this page.')

def user_is_verified(user):
    return True if user.is_authenticated else False


