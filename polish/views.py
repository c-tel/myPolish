import json

from django.shortcuts import render, get_object_or_404
from polish.models import add_user, User, not_reserved, Session, get_lesson_stuff
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect


def main(request):
	if request.user is not None:
		return HttpResponseRedirect('/home')
	return HttpResponseRedirect('/welcome')
	

def welcome(request):
	if request.user is not None:
		return HttpResponseRedirect('/home')
	return render(request, 'welcome.html',{})
	
def home(request):
	if request.user is None:
		return HttpResponseRedirect('/welcome')
	return render(request, 'home.html',{})

def signup(request):
	if request.method == 'POST':
		dict = json.loads(request.body.decode('utf-8'))
		username = dict['username']
		password = dict['password']
		if not_reserved(username):
			user = add_user(username, password)
			key = Session.objects.autentificate(username, password)
			response = JsonResponse({'status': 'ok'})
			response.set_cookie('sessid', key)
			return response
		return JsonResponse({'status': 'error'})


@csrf_exempt						
def login(request):
	dict = json.loads(request.body.decode('utf-8'))
	username = dict["username"]
	password = dict["password"]
	key = Session.objects.autentificate(username, password)
	if key:
		response = JsonResponse({
			'status':'ok'
			})
		response.set_cookie('sessid', key)
		return response
	return JsonResponse({
			'status': 'error',
			})
			
@csrf_exempt
def logout(request):
	Session.objects.exit(request.session)
	return JsonResponse({
			'status': 'ok'
			})

def validate_username(request):
	return JsonResponse({'status': 'ok',
						'valid': not_reserved(json.loads(request.body.decode('utf-8'))['username'])
						})
@csrf_exempt
def lesson(request):
	dict = json.loads(request.body.decode('utf-8'))
	num = dict['num']
	res = get_lesson_stuff(num)
	res['status'] = 'ok'
	return JsonResponse(res)