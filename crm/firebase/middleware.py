from django.http import JsonResponse
from firebase_admin import auth
from django.utils.deprecation import MiddlewareMixin
from crm.models import AdminUser
from django.urls import resolve


class FirebaseAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        resolver_match = request.resolver_match
        auth_header = request.headers.get("Authorization")
        resolver_match = resolve(request.path_info)
        if (
            request.method == "POST"
            and resolver_match
            and resolver_match.app_name == "crm"
        ):
            if auth_header:
                try:
                    token = auth_header.split("Bearer ")[1]
                    decoded_token = auth.verify_id_token(token, clock_skew_seconds=10)
                    request.user, created = AdminUser.objects.get_or_create(
                        uid=decoded_token["uid"]
                    )
                except Exception as e:
                    return JsonResponse({"message": "Invalid token"}, status=401)
            else:
                return JsonResponse({"message": "Invalid header"}, status=401)
        return None
