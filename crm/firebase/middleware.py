from django.http import JsonResponse
from firebase_admin import auth
from django.utils.deprecation import MiddlewareMixin


class FirebaseAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        resolver_match = request.resolver_match
        auth_header = request.headers.get('Authorization')
        if resolver_match and resolver_match.app_name == 'crm' and auth_header:
            try:
                token = auth_header.split("Bearer ")[1]
                decoded_token = auth.verify_id_token(token, clock_skew_seconds=10)
                request.user = decoded_token
            except Exception as e:
                print(e)
                return JsonResponse({"message": "Invalid token"}, status=401)

        return None