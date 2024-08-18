from kubernetes import client, config

config.load_kube_config()


def update_deployment(namespace, name, deployment):
    k8sApi = client.AppsV1Api()
    # patch the deployment
    k8sApi.patch_namespaced_deployment(name, namespace, deployment)

def update_resource(namespace, deployment_name, limit=0, request=0, claim="cpu", ):
    k8sApi = client.AppsV1Api()
    deployment = k8sApi.read_namespaced_deployment(deployment_name, namespace)
    
    requests={claim: "{}m".format(request)}
    limits  ={claim: "{}m".format(limit) }
    resource = client.V1ResourceRequirements(limits=limits, requests=requests)
    deployment.spec.template.spec.containers[0].resources = resource
    
    update_deployment(namespace, deployment_name, deployment)

def scale(name, namespace, replicas):
    k8sApi = client.AppsV1Api()
    k8sApi.patch_namespaced_deployment_scale(name, namespace, body={'spec': {'replicas': replicas}})
    
def bandwith(namespace, deployment_name, value = None):
    k8core = client.CoreV1Api()
    annotations = [{
            'op': "remove" if value == None else "add",  # You can try different operations like 'replace', 'add' and 'remove'
            'path': '/metadata/annotations',
            'value': {'kubernetes.io/egress-bandwidth': value}
        }]
    r = k8core.list_namespaced_pod(namespace=namespace, label_selector="app={}".format(deployment_name))
    name = r.items[0].metadata.name
    print("Pod: {} with bandwith {}".format(name, value))
    k8core.patch_namespaced_pod(name=name, namespace=namespace, body=annotations)

    
    
def setEnv(namespace, deployment_name, variable, value = None):
    k8sApi = client.AppsV1Api()
    
    deployment = k8sApi.read_namespaced_deployment(deployment_name, namespace)
    envs = deployment.spec.template.spec.containers[0].env
    #print(envs)
    if envs:
        i = 0
        found = False
        for v in envs:
            if v.name == variable and value == None:
                envs.pop(i)
                found = True
                deployment.spec.template.spec.containers[0].env = envs
                k8sApi.replace_namespaced_deployment(deployment_name, namespace, deployment)
                return
            elif v.name == variable:
                envs[i].value = value
                found = True
                break
            i += 1
        
        env = client.V1EnvVar(name=variable, value="{}".format(value))        
        deployment.spec.template.spec.containers[0].env.append(env)

    elif value:
        env = client.V1EnvVar(name=variable, value="{}".format(value))
        deployment.spec.template.spec.containers[0].env = [env]
   
    update_deployment(namespace, deployment_name, deployment)

