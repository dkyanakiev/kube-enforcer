from jinja2 import Environment, FileSystemLoader
import os
import logging
import tempfile
from templates import TemplateFinder
from kubones import Kubones
from renderer import Renderer

logger = logging.getLogger('kube-enforcer.main')

class KubeEnforce():
    def __init__(self):
        self.templates_dir = os.getenv('TEMPLATES')
        self.env_scope = os.getenv('DEPLOY_ENV')
        self.temp_config = TemplateFinder() 
        self.renderer = Renderer()
        self.kubone = Kubones()
        # self.file_loader = FileSystemLoader(templates_dir)

        
    def enforce_templates(self):
        '''
        Checks if the environment exists within the templates,
        Renders each template within the matching environment
        '''

        if self.temp_config.check_for_env():
            
            existing_ns_list = self.temp_config.get_namespaces()
            for ns in existing_ns_list:
                if not self.kubone.check_for_namespace(ns):
                    self.kubone.create_namespace(ns)

                current_template_dir = os.path.join(self.templates_dir,self.env_scope,ns)
                template_list = []
                for r, d, f in os.walk(current_template_dir):
                    for file in f:
                        if '.yaml' in file:
                            template_list.append(file)
                

                for _ in template_list:
                    print(_)
                    template = self.renderer.template_render(current_template_dir,self.env_scope,_,ns)

                    if template is not None:
                        z, rendered_filepath = tempfile.mkstemp()    
                        with open(rendered_filepath, 'w') as rf:
                            print(template, file=rf)

                        logger.debug('rendered file : %r', template)
                        self.kubone.apply_kube_yaml(rendered_filepath)
                    
                    
            
    def run(self):
        self.enforce_templates()
            

    

