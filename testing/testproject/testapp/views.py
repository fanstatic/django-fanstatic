from django.http import HttpResponseServerError
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from testproject.testapp.resource import a_css,error_css


def index(request):
    a_css.need()
    return render_to_response('testapp/index.html')


def gen_error(request):
    a_css.need()

    raise Exception()


def error(request):
    error_css.need()
    return HttpResponseServerError(content=render_to_string('testapp/error.html'))
