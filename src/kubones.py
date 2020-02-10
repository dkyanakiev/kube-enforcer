import logging
import os
import sh

logger = logging.getLogger('kubones.commands')


class Kubones:
    def __init__(self):
        self.kubectl = sh.kubectl.bake( '--v=3')

    def apply_kube_yaml(self,yaml_path):
        '''
            @yaml_path - Location of the config that you want to apply
            Apply a kube config via `kubectl apply -f <file>`
        '''

        self.run_kubectl_command('apply', '-f', yaml_path)

    def check_for_namespace(self,ns):
        '''
            @ns - Name of the namespace you wish to check
            Check if the namespace exists and return True or False
        '''
        command_ns = ['get','namespaces','-o=custom-columns=NAME:.metadata.name']
        namespace_list = (self.run_kubectl_command(command_ns)).splitlines()

        if ns in namespace_list:
            logger.info('Namespace: %s exists', ns)
            return True
        else:
            logger.warning('Namespace: %s missing',ns)
            return False

    def create_namespace(self,ns):
        '''
            @ns - Name of the namespace you wish to check
            Check if the namespace exists and return True or False
        '''
        command_ns = ['create','namespace',ns]
        self.run_kubectl_command(command_ns)


    def run_kubectl_command(self, *args):
        '''
        Run a kubectl command
        @return void
        '''
        command = ' '.join(str(arg) for arg in args)
        try:
            result = self.kubectl(*args)
            logger.info('command: %s, EXIT_CODE: %s', command, result.exit_code)
            logger.info('command: %s, STDOUT: %s', command, result.stdout.decode('utf-8'))
            #print(result)
            if result.stderr and result.exit_code != 0:
                logger.info('command: %s, STDERR: %s', command, result.stderr.decode('utf-8'))
            return result.stdout.decode('utf-8')
        except sh.ErrorReturnCode as error:
            stderr = error.stderr.decode('utf-8')
            if 'AlreadyExists' not in stderr:
                raise error
            else:
                logger.debug('Counting as a successful command since the "error" is for the '
                    'resource already existing. command: %s, STDERR: %s', command, stderr)

    

#x = Kubones()

#x.check_for_namespace()