from django.http import JsonResponse


def api_response(success, status_code, message, data=None):
    return JsonResponse(
        {"success": success, "status": status_code, "message": message, "data": data},
        status=status_code,
    )
