from django.shortcuts import render_to_response

from testproject.testapp.resource import a_css


def index(request):
    a_css.need()
    return render_to_response('testapp/index.html')


def gen_error(request):
    a_css.need()

    raise Exception()


def error(request):
    return render_to_response('testapp/error.html')

