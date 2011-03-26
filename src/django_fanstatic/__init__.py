import fanstatic

class FanstaticMiddleware(object):

    def process_request(self, request):
        # XXX config.
        fanstatic.init_needed(base_url='/')

    def process_response(self, request, response):
        # XXX response checking.
        needed = fanstatic.get_needed()
        if needed.has_resources():
            response.content= needed.render_topbottom_into_html(response.content)
        return response

