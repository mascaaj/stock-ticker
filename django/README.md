# Web development

This is stock portfolio monitoring website, create using multiple frameworks

## Access to stock data
- Currently (circa March 2022) Finnhub is being used for realtime data
- User will have to sign up and obtain the api key before getting started.
- For security purposes, it is recommended to set the key as an environment vaiable.

    ``` export FINHUB_API_KEY=<your_key_here>```

## Django, Python, Bootstrap

- Using the ```environment.yml``` file, create a conda environment

    ``` conda env create -f webdevelopment.yml```

- Conversely create a python environment (newer is better, currently developed with 3.9) and pip install the packages from ```requirements.txt```. Once installed run the server

    ```python manage.py runserver```

- Migrations might be needed in a new environment

    ```python manage.py migrate```

- Once running, navigate to ```localhost:8000``` and test the application

- For access across the LAN, add the hostname / ip address to the ```settings.py KNOWN_HOSTS```:

    ```python manage.py runserver 0.0.0.0:8000```

## @todo
- DockerFile, docker container
- Class implementation of ```views.py```
- Add tests
- Add linter
- Integrate CI
- Refactor folder structure for multiple languages
