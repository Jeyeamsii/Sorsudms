from functools import wraps
from django.http import HttpResponseForbidden

def role_required(allowed_roles):
    """
    Decorator to restrict access based on user roles.
    :param allowed_roles: List of role names allowed to access the view.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Assuming the user has a single role (ForeignKey relationship)
            user_role = request.user.role.name if request.user.role else None
            if user_role not in allowed_roles:
                return HttpResponseForbidden("Access Denied: You do not have the required role to access this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
