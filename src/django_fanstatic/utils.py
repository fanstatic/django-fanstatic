import glob
import os
import re
import fanstatic

class ResourceSettings(object):

    def __init__(self,name=None,file=None,depends=[],**kwargs):
        """
            A container for processing resource settings before handing it off to fanstatic
        """
        self.name=name
        self.file=file
        self.depends = depends
        self.other_settings=kwargs


    def update_with(self,other):
        if self.file != other.file:
            raise Exception("Resource configuration: Can not merge setting of different files (current: '%s', updating with: '%s')" %
                    (self.file,other.file))
        self.name=other.name
        self.depends = other.depends
        self.other_settings = other.other_settings


    def __repr__(self):
        return "ResourceSettings (name=%s , file=%s)"% (self.name,self.file)


    def __str__(self):
        return "ResourceSettings (name=%s , file=%s)"% (self.name,self.file)



def create_resource_settings_from_config(config,base_dir):
    """ returns a list of ResourceSettings objects based on a config line
    """
    kwargs = {}
    if isinstance(config,basestring):
        return [ResourceSettings(file=config)]
    elif config.get("file_pattern") is not None:
        if config.get("file") is not None:
            raise Exception("Resource configuration: file and file_pattern settings are mutually exclusive (name='%s', file='%s',file_pattern='%s')" %
                (config.get("name"),config.get("file"),config.get("file_pattern")))

        init_param = dict(**config)
        del init_param["file_pattern"]

        black_list = config.get("depends",[])

        ret = []
        for f in glob.iglob(os.path.join(base_dir,config["file_pattern"])):
            f = os.path.relpath(f,base_dir)
            if f not in black_list:
                ret.append(ResourceSettings(file=f,**init_param))

        return ret
    else:
        return [ResourceSettings(**config)]


def register_resources_by_config(library,config_list,auto_add_to_this_module=None):
    """
      Creates resources according a declarative configuration list.

      library : Fanstatic library to add the resources to.
      config_list: a list of the following format
       [
            "file.css",
            { "file": "homepage.js" , "depends" : ["base.js"] }
            { "file_pattern" : "css/*" , "depends" : ["css/reset.css"] }, # use filename wild card patters
            { "name" : "jquery","file" : "js/libs/jquery-1.6.2.min.js" }, # give something a name for short referral
            { "file" : "js/libs/css3-mediaqueries.js", "renderer" : some_renderer }, # all other options Fanstatic offers
            { "file_pattern" : "js/libs/jquery.*", "depends"  : ["jquery","js/swatches.js","js/plugins.js" ] },
            { "file" : "js/init.js",bottom=True },
            
       ]

       The list may contain:
        - a string representing a file name relative to the library base folder. That would create a resource for that file
        - a dictionary with the following keys:
            name - the name of the resrouces. if missing a default name will be derived from the file name
            file - a file name (relative to the librry base folder)
            file_pattern - as an alternative to file, use wildcard filename patterns to give multiple files the same settings
            depends - a list of files or names of resources to depend on. Note that these should be previously defined.
            any other key is given straight to Fanstatic Resource object.

        NOTE: The list may contain duplicate settings for the same, either explicitly or through a wildcard construction.
              The *last* settings will be used to actually create the resource.


       auto_add_to_this_module : an optional python module to add create resources to. Use this if you want to also
         use the resources from python code.
    """

    resource_settings_list = []
    resource_settings_by_filename= {}
    resource_settings_by_name = {}

    # build an ordered resource settings list
    for config in config_list:
        new_resource_settings_list = create_resource_settings_from_config(config,library.path)
        for rs in new_resource_settings_list:
            existing = resource_settings_by_filename.get(rs.file)
            if existing:
                existing.update_with(rs)
            else:
                resource_settings_list.append(rs)
                resource_settings_by_filename[rs.file]=rs


    # build resolving lists by name. Must be done now as names can change:
    for rs in resource_settings_list:
        if rs.name:
            resource_settings_by_name[rs.name] =rs


    ### process of creating:
    # 1. Now we have a  list of resource_settings
    # 2. When picking a resource it is marked as "BEING_CREATED"
    # 3. When resource is created, it's dependencies are resolved
    #     a. First one looks up in already created resources (by file/name)
    #     b. Then one looks for resource settings and creates them by going to step 2
    # 4. Created resource object is filed for dependency lookup and "BEING_CREATED" mark is removed.
    #

    resource_by_filename ={}
    resource_by_name = {}

    def _store_resrouce(rs,r):
        if rs.name:
            resource_by_name[rs.name]=r
        resource_by_filename[rs.file]=r

    def _get_resource(key):
        ret = resource_by_filename.get(key)
        if not ret:
            ret = resource_by_name.get(key)
        return  ret

    def _get_resource_settings(key):
        ret = resource_settings_by_filename.get(key)
        if not ret:
            ret = resource_settings_by_name.get(key)
        return  ret


    _create_resource = None # placeholder

    def _resolve_dep(for_rs,dep):
        """ resolves dependency lists in to real Resource objects
        """
        if isinstance(dep,basestring):
            already_defined = _get_resource(dep)
            if already_defined == "BEING_CREATED":
                raise Exception("Configuration of %s creates a circular dependency with %s" % (for_rs.file,dep))

            if already_defined:
                return  already_defined

            ## go for settings...
            dep_rs = _get_resource_settings(dep)
            if dep_rs is None:
                raise Exception("Configuration of %s requires an unknown resource: %s" % (for_rs.file,dep))
            return _create_resource(dep_rs)
        else:
            return dep # dependency is something I don't understand . Probably a fanstatic.Resource


    def _create_resource(rs,ignore_if_existing=False):
        already_defined = _get_resource(rs.file)
        if already_defined:
            if not ignore_if_existing:
                raise Exception("Duplicate definition of %s" % (rs.file,))
            return already_defined

        _store_resrouce(rs,"BEING_CREATED")

        depends = [_resolve_dep(rs,d) for d in rs.depends]

        #logger.info("Creating fantastic resource for %s",rs.file)
        r = fanstatic.Resource(library,rs.file,depends=depends,**rs.other_settings)

        # replace settings with real resource in lookup dictionaries for dependency normalization
        _store_resrouce(rs,r)

        if auto_add_to_this_module:
            name = rs.name
            if not name:
                # auto generate
                name= re.sub("[^\w]","_",rs.file)
            auto_add_to_this_module.__dict__[name]=r

        return r

    #add things to fanstatic
    for rs in resource_settings_list:
        _create_resource(rs,ignore_if_existing=True) # may have been created by dependencies.







def build_default_config_from_folder(base_folder):
    """
        Recursively scans a folder for files with an extension known to Fanstatic, returning a config list.
        The config list is of the format acceptable by register_resources_by_config above.
    """
    ret =[]
    reg = "|".join(["^[^.].*"+re.escape(ext)+"$" for ext in fanstatic.core.inclusion_renderers.keys()])
    reg = re.compile(reg)

    for (cur_dir,dirs,files) in os.walk(base_folder):
        for f in files:
            if not reg.match(f):
                continue # unknown file name
            rel_path = os.path.relpath(os.path.join(cur_dir,f),base_folder)
            ret.append(rel_path)

    return ret
