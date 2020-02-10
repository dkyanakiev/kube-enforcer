from jinja2 import Environment, FileSystemLoader
import os
import logging
import tempfile
from templates import TemplateFinder
from kubones import Kubones

logger = logging.getLogger('renderer')

class Renderer:
    def __init__(self):
        self.templates_dir = os.getenv('TEMPLATES')
        self.env_scope = os.getenv('DEPLOY_ENV')
        self.temp_config = TemplateFinder() 
    

    @staticmethod
    def template_render(template_dir,env_scope,template_name,namespace):
        '''
        Render a template
        @template_dir - full path of the location for the template it needs to render
        @env_scope - the environment value that will be rendered on top of the template
        @template_name - name of the template to render
        @namespace - name of the namespace that will be rendered on the template
        '''
        file_loader = FileSystemLoader(template_dir)
        render_env = Environment(loader=file_loader)
        get_template = render_env.get_template(template_name)
        
        render_output = get_template.render(env=env_scope,ns=namespace)
        return render_output