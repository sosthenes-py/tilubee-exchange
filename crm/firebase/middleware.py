from django.http import JsonResponse
from firebase_admin import auth
import jwt

class FirebaseAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header:
            try:
                token = auth_header.split(" ")[1]
                decoded_token = auth.verify_id_token(token)
                request.user = decoded_token
            except Exception as e:
                return JsonResponse({"error": "Invalid token"}, status=401)

        return self.get_response(request)
