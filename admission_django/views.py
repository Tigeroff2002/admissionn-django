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
        
@csrf_exempt
def get_all_directions(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        abiturient_id = data.get('abiturient_id')
        token = data.get('token')

        try:
            local_abiturient = abiturient.objects.get(id=abiturient_id)
            if local_abiturient.token != token:
                return JsonResponse({
                    'content': None,
                    'result': False,
                    'failure_message': "Tokens not equal. Go to login page"
                }, status=400)

            directions = direction.objects.all()
            if not directions.exists():
                return JsonResponse({
                    'abiturient_id': local_abiturient.id,
                    'token': token,
                    'content': {'directions': []},
                    'failure_message': None,
                    'result': True
                }, status=200)

            directions_list = [
                {'direction_id': d.id, 'direction_caption': d.caption}
                for d in directions
            ]

            return JsonResponse({
                'abiturient_id': local_abiturient.id,
                'token': token,
                'content': {'directions': directions_list},
                'failure_message': None,
                'result': True
            }, status=200)

        except abiturient.DoesNotExist:
            return JsonResponse({
                'content': None,
                'result': False,
                'failure_message': "User with such id not already existed"
            }, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def get_direction_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        abiturient_id = data.get('abiturient_id')
        token = data.get('token')
        direction_id = data.get('direction_id')

        try:
            local_abiturient = abiturient.objects.get(id=abiturient_id)
            if local_abiturient.token != token:
                return JsonResponse({
                    'content': None,
                    'result': False,
                    'failure_message': "Tokens not equal. Go to login page"
                }, status=400)

            local_direction = direction.objects.get(id=direction_id)
            places = abiturient_direction_link.objects.filter(direction_id=direction_id)

            places_list = []
            for place in places:
                abiturient_link = abiturient.objects.get(id=place.abiturient_id)
                places_list.append({
                    'place': place.place,
                    'abiturient_id': abiturient_link.id,
                    'abiturient_name': f"{abiturient_link.first_name} {abiturient_link.second_name}",
                    'mark': place.mark,
                    'admission_status': place.admission_status,
                    'prioritet_number': place.prioritet_number,
                    'has_diplom_original': place.has_diplom_original
                })

            content = {
                'direction_id': local_direction.id,
                'direction_caption': local_direction.caption,
                'budget_places_number': local_direction.budget_places_number,
                'min_ball': local_direction.min_ball,
                'places': places_list
            }

            return JsonResponse({
                'abiturient_id': local_abiturient.id,
                'token': token,
                'content': content,
                'failure_message': None,
                'result': True
            }, status=200)

        except (abiturient.DoesNotExist, direction.DoesNotExist):
            return JsonResponse({
                'content': None,
                'result': False,
                'failure_message': "No abiturient or direction with provided id found"
            }, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def add_new_direction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        abiturient_id = data.get('abiturient_id')
        token = data.get('token')
        direction_caption = data.get('direction_caption')
        budget_places_number = data.get('budget_places_number')
        min_ball = data.get('min_ball')

        try:
            local_abiturient = abiturient.objects.get(id=abiturient_id)
            if local_abiturient.token != token:
                return JsonResponse({
                    'content': None,
                    'result': False,
                    'failure_message': "Tokens not equal. Go to login page"
                }, status=400)

            if not local_abiturient.is_admin:
                return JsonResponse({
                    'content': None,
                    'result': False,
                    'failure_message': "User does not have admin privileges"
                }, status=400)

            if direction.objects.filter(caption=direction_caption).exists():
                return JsonResponse({
                    'content': None,
                    'result': False,
                    'failure_message': f"Direction with caption {direction_caption} already exists"
                }, status=400)

            local_direction = direction.objects.create(
                caption=direction_caption,
                budget_places_number=budget_places_number,
                min_ball=min_ball
            )

            return JsonResponse({
                'abiturient_id': local_abiturient.id,
                'token': token,
                'direction_id': local_direction.id,
                'content': None,
                'failure_message': None,
                'result': True
            }, status=200)

        except abiturient.DoesNotExist:
            return JsonResponse({
                'content': None,
                'result': False,
                'failure_message': "User with provided id does not exist"
            }, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def add_abiturient_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        abiturient_id = data.get('abiturient_id')
        token = data.get('token')
        content = data.get('content')

        local_abiturient = abiturient.objects.filter(id=abiturient_id).first()
        if not abiturient:
            return JsonResponse(
                {"content": None, 
                 "result": False, 
                 "failure_message": 
                 f"User with id {abiturient_id} not already existed"}, 
                 status=400)

        if local_abiturient.token != token:
            return JsonResponse(
                {"content": None, 
                 "result": False, 
                 "failure_message": "Tokens not equals. Go to login page"}, 
                 status=400)

        if not local_abiturient.is_admin:
            return JsonResponse(
                {"content": None, 
                 "result": False, 
                 "failure_message": f"User with id {abiturient_id} has not admin privileges"}, 
                 status=400)

        target_abiturient_id = content.get('target_abiturient_id')

        target_abiturient = abiturient.objects.filter(id=target_abiturient_id).first()
        if not target_abiturient:
            return JsonResponse(
                {"content": None, 
                 "result": False, 
                 "failure_message": 
                 f"User with id {target_abiturient_id} not already existed"}, 
                 status=400)

        if target_abiturient.is_requested:
            return JsonResponse(
                {"content": None, 
                 "result": False, 
                 "failure_message": 
                 f"User with id {target_abiturient_id} is already requested"}, 
                 status=400)

        target_abiturient.has_diplom_original = content.get('has_diplom_original')

        directions_links = content.get('directions_links')

        for link in directions_links:
            direction_id = link.get('direction_id')
            existed_direction = direction.objects.filter(id=direction_id).first()

            if not existed_direction:
                return JsonResponse(
                    {"content": None, 
                     "result": False, 
                     "failure_message": 
                     f"Direction with id {direction_id} not already existed"}, 
                     status=400)

            abiturient_direction_link.objects.create(
                abiturient_id=target_abiturient_id,
                direction_id=direction_id,
                place=0,
                mark=0,
                admission_status='request_in_progress',
                prioritet_number=link.get('prioritet_number'),
                has_diplom_original=content.get('has_diplom_original')
            )

        target_abiturient.is_requested = True
        target_abiturient.save()

        return JsonResponse(
            {"content": None, 
             "failure_message": None, 
             "result": True})

@csrf_exempt
def add_original_diplom(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        abiturient_id = data.get('abiturient_id')
        token = data.get('token')
        target_abiturient_id = data.get('target_abiturient_id')
        has_diplom_original = data.get('has_diplom_original')

        local_abiturient = abiturient.objects.filter(id=abiturient_id).first()
        if not abiturient:
            return JsonResponse(
                {"content": None, 
                 "result": False, 
                 "failure_message":
                   f"User with id {abiturient_id} not already existed"}, 
                   status=400)

        if local_abiturient.token != token:
            return JsonResponse(
                {"content": None, 
                 "result": False, 
                 "failure_message": "Tokens not equal. Go to login page"}, 
                 status=400)

        if not local_abiturient.is_admin:
            return JsonResponse(
                {"content": None, 
                 "result": False, 
                 "failure_message": 
                 f"User with id {abiturient_id} has no admin privileges"}, 
                 status=400)

        target_abiturient = abiturient.objects.filter(id=target_abiturient_id).first()
        if not target_abiturient:
            return JsonResponse(
                {"content": None, 
                 "result": False, 
                 "failure_message": 
                 f"User with id {target_abiturient_id} not already existed"}, 
                 status=400)

        if not target_abiturient.is_requested:
            return JsonResponse(
                {"content": None, 
                 "result": False, 
                 "failure_message": 
                 f"User with id {target_abiturient_id} was not already requested"}, 
                 status=400)

        target_abiturient.has_diplom_original = has_diplom_original
        target_abiturient.save()

        return JsonResponse({"content": None, "failure_message": None, "result": True})
    
@csrf_exempt
def get_all_abiturients(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        abiturient_id = data.get('abiturient_id')
        token = data.get('token')

        local_abiturient = abiturient.objects.filter(id=abiturient_id).first()
        if not local_abiturient:
            return JsonResponse(
                {"content": None, 
                 "result": False, 
                 "failure_message": 
                 f"User with id {abiturient_id} not already existed"}, 
                 status=400)

        if local_abiturient.token != token:
            return JsonResponse(
                {"content": None, 
                 "result": False, 
                 "failure_message": "Tokens not equal. Go to login page"}, 
                 status=400)

        if not local_abiturient.is_admin:
            return JsonResponse(
                {"content": None, 
                 "result": False, "failure_message": 
                 f"User with id {abiturient_id} has no admin privileges"}, 
                 status=400)

        abiturients_db = abiturient.objects.exclude(is_admin=True)
        abiturients = [
            {
                "abiturient_id": item.id,
                "abiturient_name": f"{item.first_name} {item.second_name}",
                "is_requested": item.is_requested,
                "is_enrolled": item.is_enrolled,
                "has_diplom_original": item.has_diplom_original,
            } for item in abiturients_db
        ]

        content = {"abiturients": abiturients}
        return JsonResponse(
            {"abiturient_id": abiturient_id, 
             "token": token, 
             "content": content, 
             "failure_message": None, 
             "result": True})
    
@csrf_exempt
def get_enrolled_abiturients(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        abiturient_id = data.get('abiturient_id')
        token = data.get('token')

        local_abiturient = abiturient.objects.filter(id=abiturient_id).first()
        if not local_abiturient:
            return JsonResponse(
                {"content": None, 
                 "result": False, 
                 "failure_message": 
                 f"User with id {abiturient_id} not already existed"}, 
                 status=400)

        if local_abiturient.token != token:
            return JsonResponse(
                {"content": None, 
                 "result": False, 
                 "failure_message": "Tokens not equal. Go to login page"}, 
                 status=400)

        if not local_abiturient.is_admin:
            return JsonResponse(
                {"content": None, 
                 "result": False, 
                 "failure_message": 
                 f"User with id {abiturient_id} has no admin privileges"}, 
                 status=400)

        abiturients_db = abiturient.objects.filter(is_enrolled=True).exclude(is_admin=True)
        abiturients = [
            {
                "abiturient_id": item.id,
                "abiturient_name": f"{item.first_name} {item.second_name}",
                "is_requested": item.is_requested,
                "is_enrolled": item.is_enrolled,
                "has_diplom_original": item.has_diplom_original,
            } for item in abiturients_db
        ]

        content = {"abiturients": abiturients}
        return JsonResponse(
            {"abiturient_id": abiturient_id, 
             "token": token, 
             "content": content, 
             "failure_message": None, 
             "result": True})