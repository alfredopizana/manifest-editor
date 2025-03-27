# manifest-editor

Start Project
```
streamlit run app.py
```

Freeze Packages on venv
```
pip freeze -l > requirements.txt
```


###Build a Docker image
```
docker build -t manifest-editor .
```

Run the Docker container
```
docker run -p 8501:8501 manifest-editor
```