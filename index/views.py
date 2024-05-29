from django.http import JsonResponse

# Create your views here.
def index(request):
    return JsonResponse({'message': 'Hello, World!'})