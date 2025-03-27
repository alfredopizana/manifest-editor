### Building and running your application

When you're ready, start your application by running:
`docker compose up --build`.

Your application will be available at http://localhost:8000.

### Deploying your application to the cloud

First, build your image, e.g.: `docker build -t myapp .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.

Then, push it to your registry, e.g. `docker push myregistry.com/myapp`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.


###Build a Docker image
```
docker build -t streamlit .
```

Run the Docker container
```
docker run -p 8501:8501 streamlit
```


To view your app, users can browse to http://0.0.0.0:8501 or http://localhost:8501

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)
* [Streamlit Guide](https://docs.streamlit.io/deploy/tutorials/docker)
* 