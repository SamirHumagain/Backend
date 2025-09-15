import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

KHALTI_SECRET_KEY = "cf225d50fa7c4f48a23b977e82f211b8"  # Replace with your actual secret key

@csrf_exempt
def initiate_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # Use test endpoint for development
        url = "https://dev.khalti.com/api/v2/epayment/initiate/"
        headers = {
            "Authorization": f"Key {KHALTI_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        # Ensure amount is integer
        if "amount" in data:
            data["amount"] = int(data["amount"])
        # Log request and response for debugging
        print("Khalti Payment Request:", data)
        response = requests.post(url, json=data, headers=headers)
        print("Khalti Response Status:", response.status_code)
        print("Khalti Response Content:", response.text)
        try:
            return JsonResponse(response.json())
        except Exception:
            return JsonResponse({"error": "No response or invalid response from Khalti", "status_code": response.status_code, "content": response.text}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)
