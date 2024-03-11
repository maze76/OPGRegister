from django.shortcuts import redirect
from django.urls import reverse
from django.urls import resolve
from datetime import datetime, timedelta
from django.contrib import auth
from . import settings


class AutoLogout:
    """
    Auto logout of the user after time defined in settings.py
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            # If user is not authenticated, skip the logout process
            return self.get_response(request)

        # Get the last activity timestamp from the session
        last_touch = request.session.get('last_touch')
        if last_touch:
            # Convert the last_touch datetime object to string
            last_touch = datetime.strptime(last_touch, '%Y-%m-%d %H:%M:%S.%f')

            # Calculate the time elapsed since the last activity
            elapsed_time = datetime.now() - last_touch
            auto_logout_delay = timedelta(minutes=settings.AUTO_LOGOUT_DELAY)

            if elapsed_time > auto_logout_delay:
                # If the elapsed time exceeds the auto logout delay, log out the user
                auth.logout(request)
                # Redirect to the login page after logout
                return redirect(reverse('login'))

        # Update the last activity timestamp in the session
        request.session['last_touch'] = str(datetime.now())

        return self.get_response(request)
