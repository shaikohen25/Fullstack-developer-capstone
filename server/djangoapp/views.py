from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create a `login_user` view to handle sign-in requests
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({"userName": username, "status": "Authenticated"})
            return JsonResponse({"userName": username, "status": "Authentication Failed"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# Create a `logout_request` view to handle sign-out requests
def logout_request(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({"userName": "", "status": "Logged out"})
    return JsonResponse({"error": "Invalid request method"}, status=405)


# Create a `registration` view to handle sign-up requests
@csrf_exempt
def registration(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            email = data.get('email')

            if User.objects.filter(username=username).exists():
                return JsonResponse({"userName": username, "error": "Already Registered"})

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# Get list of cars
def get_cars(request):
    if request.method == 'GET':
        if not CarMake.objects.exists():
            initiate()
        car_models = CarModel.objects.select_related('car_make')
        cars = [{"CarModel": car_model.name, "CarMake": car_model.car_make.name} for car_model in car_models]
        return JsonResponse({"CarModels": cars})
    return JsonResponse({"error": "Invalid request method"}, status=405)


# Fetch dealerships
def get_dealerships(request, state="All"):
    if request.method == 'GET':
        endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
        dealerships = get_request(endpoint)
        return JsonResponse({"status": 200, "dealers": dealerships})
    return JsonResponse({"error": "Invalid request method"}, status=405)


# Render dealer reviews
def get_dealer_reviews(request, dealer_id):
    if request.method == 'GET' and dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            sentiment_response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = sentiment_response.get('sentiment', 'unknown')
        return JsonResponse({"status": 200, "reviews": reviews})
    return JsonResponse({"status": 400, "message": "Bad Request"})


# Render dealer details
def get_dealer_details(request, dealer_id):
    if request.method == 'GET' and dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    return JsonResponse({"status": 400, "message": "Bad Request"})


# Submit a review
@csrf_exempt
def add_review(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                post_review(data)
                return JsonResponse({"status": 200})
            except Exception as e:
                logger.error(f"Error posting review: {e}")
                return JsonResponse({"status": 401, "message": "Error in posting review"})
        return JsonResponse({"error": "Invalid request method"}, status=405)
    return JsonResponse({"status": 403, "message": "Unauthorized"})
