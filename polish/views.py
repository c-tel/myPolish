import json

from django.shortcuts import render, get_object_or_404
from polish.models import *
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
	return render(request, 'home.html',{'user' : request.user.username})

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

	
@csrf_exempt
def test(request):
	dict = json.loads(request.body.decode('utf-8'))
	num = dict['num']
	res = get_test_stuff(num, request.user)
	res['status'] = 'ok'
	return JsonResponse(res)


@csrf_exempt	
def addWord(request):
	dict = json.loads(request.body.decode('utf-8'))
	user = request.user
	id = dict['id']
	recordWord(id, user)
	return JsonResponse({'status':'ok'})


@csrf_exempt	
def finished(request):
	dict = json.loads(request.body.decode('utf-8'))
	user = request.user
	id = dict['id']
	next_lesson(user, id)
	return JsonResponse({'status':'ok'})

@csrf_exempt	
def lessons_info(request):
	user = request.user
	info = get_lessons_info(user)
	return JsonResponse(info)

@csrf_exempt	
def brainstorm(request):
	return JsonResponse(review(request.user))

	
@csrf_exempt	
def day_count(request):
	return JsonResponse({'count':words_for_today(request.user)})

@csrf_exempt	
def delete_prg(request):
	drop(request.user)
	return JsonResponse({'status':'ok'})