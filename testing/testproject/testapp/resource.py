from fanstatic import Library, Resource

library = Library('testapp', 'media')

a_css = Resource(library, 'a.css')

error_css = Resource(library, 'error.css')
