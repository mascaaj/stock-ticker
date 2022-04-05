# Stock ticker with Ruby on Rails

## Installation

- Install nodejs

    ```
    sudo apt-get update
    sudo apt-get install nodejs
    ```

- Install Heroku-cli

    ```
    curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
    ```

- Install ruby and rails. This is a multistep process. For Ubuntu, I used this resource
https://gorails.com/setup/ubuntu/18.04

## Run Application

- Create an application

    ```
    rails new <application_name>
    ```

- Create a new page
    ```
    rails generate controller <controller_name> <page_name>
    ```

- Start the application

    ```
    rails server
    ```
