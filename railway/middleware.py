from django.conf import settings
from django.http import JsonResponse

class AdminAPIKeyMiddleware:
    """
    Middleware to validate API key for admin endpoints.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Check if the request path starts with admin endpoints
        if request.path.startswith('/api/railway/admin/'):
            # In Django, X-API-KEY becomes HTTP_X_API_KEY in request.META
            api_key_header = 'HTTP_' + settings.API_KEY_HEADER.replace('-', '_').upper()
            api_key = request.META.get(api_key_header, '')

            # Debug - print out all headers
            print(f"API KEY HEADER: {api_key_header}")
            print(f"API KEY VALUE: {api_key}")
            print(f"EXPECTED: {settings.API_KEY}")
            
            if api_key != settings.API_KEY:
                return JsonResponse(
                    {'error': 'Invalid or missing API key'}, 
                    status=401
                )
        
        return self.get_response(request)
