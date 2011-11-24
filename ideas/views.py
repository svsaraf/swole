from django.shortcuts import render_to_response
from ideas.models import *
from django.template import RequestContext
from django import forms
from django.http import HttpResponseRedirect
import facebook
from django.conf import settings
from django.contrib.auth import login, authenticate
import json
from django.utils import simplejson
from django.http import HttpResponse

def testthisajax(request):
    response_string="hello"
    response_dict = {}
    if request.method == u'GET':
        GET = request.GET
        if GET.has_key(u'myid'):
            idvalue = int(GET[u'myid'])
            currentuser = User.objects.get(pk=idvalue)
            w = Workout(author = currentuser)
            w.save()
            wt = WorkoutTotals.objects.get(author = currentuser)
            wt.number = wt.number + 1
            wt.save()
            response_string = "" + '<div class="workout">' + w.author.name() + " just added a workout!" + "</div>"
            response_dict.update({'workout': response_string, 'personid': currentuser.pk})
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/json')

def index(request):
    dictionary_list = getLoginInfo(request)
    newsfeed = Workout.objects.all().order_by('-created_at')
    totals = WorkoutTotals.objects.all().order_by('-number')

    return render_to_response('home.html', {
        "facebook_app_id": settings.FACEBOOK_APP_ID,
        "current_user": dictionary_list["current_user"], 
        "newsfeed": newsfeed[:25],
        "totals": totals,
        "fbid": dictionary_list["fbid"],
        }, context_instance=RequestContext(request)
    )

def json_response(obj):
    return HttpResponse(simplejson.dumps(obj), mimetype="application/x-javascript")

def getLoginInfo(request):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)
    message = ''
    user = None
    fbid = 0
    if cookie:
        try:
            up = UserProfile.objects.get(fbid=cookie['uid'])
            user = up.user
        except UserProfile.DoesNotExist:
            graph = facebook.GraphAPI(cookie["access_token"])
            profile = graph.get_object("me")

            try:
                genUser = profile['first_name'] + profile['id']
                user = User.objects.get(username=genUser)
            except User.DoesNotExist:
                user = User.objects.create_user(username=genUser, email='test@example.com', password=genUser)
                user.first_name = profile['first_name']
                user.last_name = profile['last_name']
                user.save()
                wt = WorkoutTotals(author = user, number = 0)
                wt.save()

            up = UserProfile(user=user, fbid=cookie['uid'], access_token=cookie['access_token'])
            up.save()
        user = authenticate(username=user.username, password=user.username)
        if user is not None:
            login(request, user)
            profile = UserProfile.objects.get(user=user)
            fbid = profile.pk
        else:
            print "user was none"
            fbid = 0
    else:
        message='Log in'
    parts_dict = {}
    parts_dict["message"] = message
    parts_dict["current_user"] = user
    parts_dict["fbid"] = fbid
    return parts_dict

