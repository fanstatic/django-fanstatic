import fanstatic

class FanstaticMiddleware(object):

    def process_exception(self, request, exception):
        fanstatic.get_needed().clear()
        
