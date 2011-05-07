from django.http import HttpResponse
import fanstatic
from django.core.handlers.wsgi import WSGIRequest

class FanstaticMiddleware(object):

    def __init__(self):
        config = dict()

        from settings import FANSTATIC_CONFIG
        config.update(FANSTATIC_CONFIG)

        # this is just to give useful feedback early on
        fanstatic.NeededResources(**config)

        self.config=config

        self.publisher = fanstatic.Publisher(fanstatic.get_library_registry())

        self.publisher_signature = "/"+ FANSTATIC_CONFIG.get("publisher_signature",fanstatic.DEFAULT_SIGNATURE) +"/"




    def process_request(self,request):
        if not isinstance(request,WSGIRequest):
            raise Exception("FanstaticMiddelwheres only work under a WSGI based server")

        if not request.method in ['GET', 'POST']:
            return # nothing to do

        if self.publisher_signature and request.path_info.startswith(self.publisher_signature):
            # if no publisher_signature defined, publisher is serverd from somewhere else
            response_data = {}
            def status_headers_setter(status,headers):
                response_data['status'] = int(status.split(' ')[0])
                response_data['headers'] = headers

            # strip fanstatic prefix. Publisher expects resource path.
            request.environ["PATH_INFO"] = request.environ["PATH_INFO"][len(self.publisher_signature):]

            result = self.publisher(request.environ,status_headers_setter)
            response = HttpResponse(content=result, status=response_data['status'])

            for k,v in response_data['headers']:
                response[k]=v

            return response


        needed = fanstatic.init_needed(**self.config)

        # Make sure the needed resource object is put in the WSGI
        # environment as well, for frameworks that choose to use it
        # from there.
        request.environ[fanstatic.NEEDED] = needed

    def process_response(self,request,response):

        if not isinstance(request,WSGIRequest):
            raise Exception("FanstaticMiddelwheres only work under a WSGI based server")

        if not fanstatic.NEEDED in request.environ:
            return response # life is beautiful. Nothing to do.

        needed = request.environ[fanstatic.NEEDED]

        # The wrapped application may have `needed` resources.
        if needed.has_resources():
            result = needed.render_topbottom_into_html(response.content)
            response.content=result

        return response

    def process_exception(self, request, exception):
        fanstatic.get_needed().clear()


