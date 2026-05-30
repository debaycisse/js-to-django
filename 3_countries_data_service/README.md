# Countries Data Service API System

## Introduction

This API collects a list of countries from an external API and obtains their respective currencies' exchange rate from another external API and put these data together in a cache, backed by MySQL.

It also generates a .PNG image to hold statistics of the cache at the time of checking.

The API also has an interface with which user can refresh the cache by either upating the existing country records or inserting a deleted or non-existing country records, known as upserting database operation.

This project converts the implemented version of the same project, which was done via NestJS, to Django. 

### Libraries and Frameworks

Below is a list of libraries that are utilized to achieve the implementation of this project.

- **Django**:
    
    This is the framework or the foundation on top of which every other libraries, used through out this project operate.

- **DRF (Dajngo REST Framework)**:

    This library is built on top of the Django framework for a purpose of implementing a RESTful (REprensentational State Tranfer) application program interface system.
    
    It is a major engine that powers up the implementation of this project.

- **MySQL Client**:

    The interraction between the database, used for caching in this project and the main application itself was made possible by this library.

- **Pillow**:

    This library was used to generate image canvas and add texts on it. The texts are the statistics of the records, stored in the cache.

- **Requests**:

    This library was used for sending http requests to the two external API systems, used in this project.

### Database

The database was used to cache the records of countries, fetched from an external API system and their respective exchange rates, which was also fetch from another external API.

MySQL was picked as the database of choice and used for the cache implementation, based on the original implemented (by myself during an internship program that I participated) project, converted from NestJS to Django.

## Installation

The below command helps you to install the needed library and framework to make this application available on your system.

- Download the project  by cloning it

    ```
    git clone https://github.com/debaycisse/js-to-django.git
    ```

- Then open the `3_countries_data_service` directory:
    
    ```
    cd ./3_countries_data_service
    ```

- Create a virtual environment for the installation

    To keep things well organized and avoid libraries conflicts on your system, always maintain a virtual environment for different installation of libraries of various projects. Therefore, create a virtual environment and activate the environment.

    _Note: you must make sure that `venv` is already isntalled on your system before you run the below command_

    ```
    python -m venv .venv
    ```

- Activate the virtual environment

    ```
    source .venv/bin/activate
    ```
    
- Lastly, install the required libraries

    ```
    python -m pip install -r requirements.txt
    ```
    
    You can use a shortcut of `pip install -r requirements.txt` for the installation as well.

## How to use the application

__Before you will be able to use the application, you need to run it, but you have to provide some environment variables before the app can run seamlessly__. This environment variables hold some configuration related parameters that this system needs in order to be able run.

Another important point is that you need to prepare the database for the needed tables by running the below command.

Make sure you are in the `3_countries_data_service` directory before executing the below commands on your terminal.

```
python manage.py migrate
```

These configuration related environment variables consists of database' username, password, name, port, and others.

The following must be defined in your `.env` file that holds environment variables:

- `DB_NAME` - this holds the name of the database to be used
- `DB_USERNAME` - this holds the username with which database operations can be authenticated
- `DB_PORT` - this holds the port number of the database server
- `DB_HOST` - this holds the host where the database server runs
- `DB_PASSWORD` - this holds the password for the `DB_USERNAME` username
- `COUNTRY_CACHE_KEY` - this holds string, used as the key with which cached data from the country api server is retrieved if not expired.
- `EXCHANGE_RATE_CACHE_KEY` - this holds string, used as the key with which cached data from the exchange rate api server is retrieved if not expired.
- `CACHE_TTL` - this holds the number of seconds after which cached data is expired

Finally, you can start the application, by executing the below command, provided that you have provided the mentioned environment variables.

```
python manage.py runserver
```

## Conclusion

The `bulk_create` of Django is a powerful function that ensures a multiple number of records can be inserted or updated (that is upserted) with just a single database' hit, instead of several hits based on the number of records that need to be either created or updated.

The Pillow library provides an extensive collection functions with which image can be processed and manipulated in various forms.

If you would like to use this application in production environment, don't forget to diable the `DEBUG` mode by updating its value in the `setting.py` file, set a hidden `SECRET_KEY`, configure the `ALLOWED_HOST`, enforce https, and others.
Most importantly, run `python manage.py check --deploy` so as to ensure that no security setting is missed out.

Though, this project can be further enhanced by incorporating the rate limiting, pagination, and other techniques but it was implemented strictly based on the NestJS implemented version.