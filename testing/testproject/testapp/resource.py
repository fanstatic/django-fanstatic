from fanstatic import Library, Resource

library = Library('testapp', 'media')

a_css = Resource(library, 'a.css')

fake_error_css = Resource(library,'something_that_doesnt_exist.css')
