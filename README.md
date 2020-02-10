# Kube Enforcer

This is a simple service that would enforce your K8s while rendering them at the same time.

## Description

The idea was to solve a simple use case for me.
Create have a central location for every type of k8s yaml and have a service that would enforce them while also rendering specific information on top of them.

Currently it mainly looks for the following structure:

```bash
 |--(source)
 |   |-- (environment) 
 |   |   |-- (namespace)
 |   |   |   |-- pod.yaml
 |   |   |-- (namespace)
 |   |   |   |-- pod.yaml
```
1. The service will double check if the environment exists inside the directory
2. It will check if your namespace **does not exist**, it will create it for you.
Note: Working on a flag to bypass this if a namespace.yaml exists in your repo.

## Usage

There are a few things on my TODO in order to make this more flexible.
But few things that need to be  configured in order to run this.
```bash
export DEPLOY_ENV='dev'
export TEMPLATES='/tmp/test/k8s'
```
`DEPLOY_ENV` - This is used to filter which environment are you enforcing.
With the current design the idea is to run this as a pod in each environment but keep all your configs in the same repository, so this is used in order to filter.

`TEMPLATES` - Location of your configurations. Note: This is the location you use inside your container.

With the current setup all the yamls have to be prebaked in your image.
Currently they live in `k8s/`

Example deployment: `deployment.yaml` 

## TODO:
 * [ ] Allow for external templates to be used. Example: Clone from git
 * [ ] Allow for easy use of userdata for setup in AWS EC2 hosts 
 * [ ] Write tests for the rendering and kubectl apply

Will add more as work continues


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)