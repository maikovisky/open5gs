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
    
