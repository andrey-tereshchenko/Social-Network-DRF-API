from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from api.models import User


class SetLastRequestMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated:
            User.objects.filter(pk=request.user.pk).update(last_request=timezone.now())
