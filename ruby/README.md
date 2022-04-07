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

- Install webpack by including it in gemfile
    ``` 
    bundle install
    rails install webpack
    ```

- Install jquery bootstrap and other dependencies. Most instructions out there were outdated. This worked https://martinezjf2.medium.com/installing-bootstrap-to-a-rails-project-53d3d37db702
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
