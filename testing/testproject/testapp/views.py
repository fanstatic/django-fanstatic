from django.shortcuts import render_to_response

from testproject.resource import a


def index(request):
    a.need()
    return render_to_response('testapp/index.html')
