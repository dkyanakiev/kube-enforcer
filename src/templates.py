import os
import logging


logger = logging.getLogger('kube-enforcer.templates')


class TemplateFinder:
    def __init__(self):
        self.env_scope = os.getenv('DEPLOY_ENV')
        self.template_dir = os.getenv('TEMPLATES')
        

    def check_for_env(self):
        '''
            Look at the sub directory and find if there are config templates
            for the specified environment
        '''
        env_list = os.listdir(self.template_dir)

        if self.env_scope in env_list:
            logger.info("Environment scope: {} EXISTS in the config dir {}".
            format(
                self.env_scope,
                self.template_dir
            )
            )
            return True
        else:
            logger.info("Environment scope: {} MISSING in the config dir {}".
            format(
                self.env_scope,
                self.template_dir
            )
            )
            return False        
        

    def get_namespaces(self):
        '''
            Look at the sub directory and find the name of the namespace
        '''
        sub_dir = os.path.join(self.template_dir,self.env_scope)
        namespaces = os.listdir(sub_dir)
        
        logger.info("Found the following namespaces: {}"
            .format(
                namespaces
            ))

        return namespaces






# temp = TemplateFinder()

# if temp.check_for_env():
#     print(temp.get_namespace())


#x = temp.check_for_env()
#print(x)

