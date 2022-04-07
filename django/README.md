# Web development

This is stock portfolio monitoring website, create using multiple frameworks

## Access to stock data
- Currently (circa March 2022) Finnhub is being used for realtime data
- User will have to sign up and obtain the api key before getting started.
- For security purposes, it is recommended to set the key as an environment vaiable.

    ``` export FINHUB_API_KEY=<your_key_here>```

## Django, Python, Bootstrap

- Using the `environment.yml` file, create a conda environment

    ``` conda env create -f webdevelopment.yml```

- Conversely create a python environment (newer is better, currently developed with 3.9) and pip install the packages from `requirements.txt`. Once installed run the server

    ```python manage.py runserver```

- Migrations might be needed in a new environment

    ```python manage.py migrate```

- Once running, navigate to `localhost:8000` and test the application

- For access across the LAN, add the hostname / ip address to the ```settings.py KNOWN_HOSTS```:

    ```python manage.py runserver 0.0.0.0:8000```

- Update conda installs to the environment. While both these are not needed together, historically some packages have been avaliable with pip and not with conda, having the `requirements.txt` file makes sure this is not an issue.:
    ``` 
    conda list -e > requirements.txt
    conda env export -n webdevelopment > webdevelopment.yml
    ```

- To ensure any keys do not get pushed to remote, use gittyclean pre commit:
    ``` gittyleaks --find-anything```

## Building and running the docker file:

- Ensure your FINHUB_API_KEY is created and stored as an environment variable.
- Ensure your DJANGO_ALLOWED_HOSTS is created and stored as an environment variable.

    ``` 
    cd stock-ticker
    docker build -f django.Dockerfile -t <name-image-here> .
    ```

    Container should be built, check using ```docker images```
    ```
    docker run -e FINHUB_API_KEY=$FINHUB_API_KEY -e DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS -it -p 8000:8000 stock-app
    ```

- Navigate to `<allowed_host_ip_address>:8000` in browser of choice


## @todo
- ~~Split functions into different files (functional)~~
- ~~Add suite of standard plots for each stock~~
- ~~Parametrize the time for api call~~
- ~~Class implementation of `views.py`~~
- ~~DockerFile, docker container~~
- ~~Refactor folder structure for multiple languages~~
- Seem to have added in an irregular bug : Add stocks table does not fill out 100% of the time (Test and inspect)
- Add tests
- Add linter
- Integrate CI
