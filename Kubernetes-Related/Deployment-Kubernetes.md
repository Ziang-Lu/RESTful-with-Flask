# Deployment-`Kubernetes`

Check out this video tutorial: https://www.youtube.com/watch?v=1xo-0gCVhTU&list=PLZdWBibC1pBSorj3W8RnzlKiftHvUAduh&index=3&t=0s

<img src="https://github.com/Ziang-Lu/RESTful-with-Flask/blob/master/Kubernetes-Related/Kubernetes%20Vocab.png?raw=true">

<img src="https://github.com/Ziang-Lu/RESTful-with-Flask/blob/master/Kubernetes-Related/Kubernetes%20Cluster%20Architecture.png?raw=true">

Sample `my_deployment.yml`:

```yaml
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: myappdeployment
spec:  # We deploy 5 pods.
  replicas: 5
  template:
    metadata:
      labels:
        app: myapp  # ***
    spec:
      containers:  # Each pod contains only 1 container.
        - name: myapp
          image: jamesquigley/exampleapp:v1.0.0
          ports:
            - containerPort: 8080  # ---

# Pods are "unreliable" units of work that come and go all the time.
# => As such, due to its ephemeral nature, a pod by itself is NOT ACCESSIBLE BY THE OUTSIDE WORLD.
# => Thus, we need a static resource that represents all the related pods as a single element (or, in this case, that represents the deployment responsible for these pods).

---
apiVersion: v1
kind: Service
metadata:
  name: exampleservice
spec:
  selector:
    app: myapp  # This should match the above "***".
  ports:
    - protocol: TCP
      # Port accessible inside cluster
      port: 80
      # Port to forward to inside the pod
      targetPort: 8080  # This should match the above "---"
      # Port accessible outside cluster
      nodePort: 30001
  type: LoadBalancer
```

<br>

For a written tutorial, check out https://auth0.com/blog/kubernetes-tutorial-step-by-step-introduction-to-basic-concepts/

***

Command-line tool to manage Kubernetes: `kubectl`

Kubernetes cloud providers:

* <u>Minikube</u>
* <u>Google Kubernetes Engine (GKE)</u>
* Amazon Elastic Kubernetes Service (EKC)
* Azure Kubernetes Service (AKS)
* OpenShift Kubernetes

*<u>Commonly used</u>*

***

