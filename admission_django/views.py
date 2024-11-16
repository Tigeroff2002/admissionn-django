from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import abiturient, abiturient_direction_link, direction
import json
import uuid

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('first_name')
            second_name = data.get('second_name')
            is_admin = data.get('is_admin', False)

            token = str(uuid.uuid4())

            if abiturient.objects.filter(email=email).exists():
                return JsonResponse({
                    "content": None,
                    "result": False,
                    "failure_message": "User with such email already existed"
                }, status=400)

            local_abiturient = abiturient.objects.create(
                email=email,
                password=password,
                token=token,
                first_name=first_name,
                second_name=second_name,
                is_admin=is_admin,
                has_diplom_original=False
            )

            return JsonResponse({
                "abiturient_id": local_abiturient.id,
                "token": token,
                "is_admin": is_admin,
                "content": None,
                "failure_message": None,
                "result": True
            }, status=200)

        except Exception as err:
            return JsonResponse({"error": str(err)}, status=500)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            token = str(uuid.uuid4())

            local_abiturient = abiturient.objects.filter(email=email).first()

            if not local_abiturient:
                return JsonResponse({
                    "content": None,
                    "result": False,
                    "failure_message": "User with such email not already existed"
                }, status=400)

            if local_abiturient.password != password:
                return JsonResponse({
                    "content": None,
                    "result": False,
                    "failure_message": "Passwords not equals"
                }, status=400)

            local_abiturient.token = token
            local_abiturient.save()

            return JsonResponse({
                "abiturient_id": local_abiturient.id,
                "token": token,
                "is_admin": local_abiturient.is_admin,
                "content": None,
                "failure_message": None,
                "result": True
            }, status=200)

        except Exception as err:
            return JsonResponse({"error": str(err)}, status=500)

@csrf_exempt
def logout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            abiturient_id = data.get('abiturient_id')
            token = data.get('token')

            local_abiturient = get_object_or_404(abiturient, id=abiturient_id)

            if local_abiturient.token != token:
                return JsonResponse({
                    "content": None,
                    "result": False,
                    "failure_message": "Tokens not equals. Go to login page"
                }, status=400)

            return JsonResponse({
                "abiturient_id": local_abiturient.id,
                "token": token,
                "content": None,
                "failure_message": None,
                "result": True
            }, status=200)

        except Exception as err:
            return JsonResponse({"error": str(err)}, status=500)

@csrf_exempt
def get_lk_content(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            abiturient_id = data.get('abiturient_id')
            token = data.get('token')

            local_abiturient = get_object_or_404(abiturient, id=abiturient_id)

            if local_abiturient.token != token:
                return JsonResponse({
                    "content": None,
                    "result": False,
                    "failure_message": "Tokens not equals. Go to login page"
                }, status=400)

            directions_links_db = abiturient_direction_link.objects.filter(abiturient_id=abiturient_id)

            if not directions_links_db.exists():
                content = {
                    "first_name": local_abiturient.first_name,
                    "second_name": local_abiturient.second_name,
                    "email": local_abiturient.email,
                    "has_diplom_original": local_abiturient.has_diplom_original,
                    "is_enrolled": local_abiturient.is_enrolled,
                    "directions_links": []
                }

                return JsonResponse({
                    "abiturient_id": local_abiturient.id,
                    "token": token,
                    "content": content,
                    "failure_message": None,
                    "result": True
                }, status=200)

            directions_links = []
            for current_item in directions_links_db:
                local_direction = get_object_or_404(direction, id=current_item.direction_id)
                directions_links.append({
                    "direction_id": local_direction.id,
                    "direction_caption": local_direction.caption,
                    "place": current_item.place,
                    "mark": current_item.mark,
                    "admission_status": current_item.admission_status,
                    "priotitet_number": current_item.prioritet_number
                })

            directions_links.sort(key=lambda x: x['priotitet_number'], reverse=True)

            content = {
                "first_name": local_abiturient.first_name,
                "second_name": local_abiturient.second_name,
                "email": local_abiturient.email,
                "has_diplom_original": local_abiturient.has_diplom_original,
                "is_enrolled": local_abiturient.is_enrolled,
                "directions_links": directions_links
            }

            return JsonResponse({
                "abiturient_id": local_abiturient.id,
                "token": token,
                "content": content,
                "failure_message": None,
                "result": True
            }, status=200)

        except Exception as err:
            return JsonResponse({"error": str(err)}, status=500)
