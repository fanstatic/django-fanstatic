from __future__ import absolute_import
import fanstatic
from  django import template
__author__ = 'boaz'

from django import template

register = template.Library()

@register.simple_tag
def resourceurl(resource):
    parsed_name = resource.split(u':',1)
    if len(parsed_name) == 1:
        raise template.TemplateSyntaxError(u"resource name must of the following syntax: library_name:rel_path_to_resource. Got '%s'." %
                                           (resource,))

    fs_lib = fanstatic.get_library_registry().get(parsed_name[0])
    needed = fanstatic.get_needed()
    return needed.library_url(fs_lib)+"/"+parsed_name[1]



@register.simple_tag
def need(resource):
    """ mark a fantastic resource as needed
    """
    parsed_name = resource.split(u':',1)
    if len(parsed_name) == 1:
        raise template.TemplateSyntaxError(u"resource name must of the following syntax: library_name:rel_path_to_resource. Got '%s'." %
                                           (resource,))

    fs_lib = fanstatic.get_library_registry().get(parsed_name[0])
    if fs_lib is None:
        raise template.TemplateSyntaxError(u"Library %s is not registered with fanstatic."% (parsed_name[0],))
    fs_resource = fs_lib.known_resources.get(parsed_name[1])
    if fs_resource is None:
        raise template.TemplateSyntaxError(u"resource '%s' is not registered with library '%s'."%(parsed_name[1],parsed_name[0]))

    fs_resource.need()
    
    return ""
