# Deployment-`Kubernetes`

Check out this video tutorial: https://www.youtube.com/watch?v=1xo-0gCVhTU&list=PLZdWBibC1pBSorj3W8RnzlKiftHvUAduh&index=3&t=0s

<img src="https://github.com/Ziang-Lu/RESTful-with-Flask/blob/master/Kubernetes%20Vocab.png?raw=true">

<img src="https://github.com/Ziang-Lu/RESTful-with-Flask/blob/master/Kubernetes%20Cluster%20Architecture.png?raw=true">

Sample `kubernetes-deployment.yml`:

```yaml
---
kind: Service
apiVersion: v1
metadata:
  name: exampleservice
spec:
  selector:
    app: myapp
  ports:
    - protocol: "TCP"
      # Port accessible inside cluster
      port: 8081
      # Port to forward to inside the pod
      targetPort: 8080
      # Port accessible outside cluster
      nodePort: 30002
  type: LoadBalancer



---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: myappdeployment
spec:
  replicas: 5
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: jamesquigley/exampleapp:v1.0.0
          ports:
            - containerPort: 8080
```

For a written tutorial, check out https://auth0.com/blog/kubernetes-tutorial-step-by-step-introduction-to-basic-concepts/

