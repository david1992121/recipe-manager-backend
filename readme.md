[![CI](https://github.com/david1992121/recipe-manager-backend/actions/workflows/ci.yml/badge.svg)](https://github.com/david1992121/recipe-manager-backend/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/david1992121/recipe-manager-backend/branch/main/graph/badge.svg?token=r0XZ8mDmON)](https://codecov.io/gh/david1992121/recipe-manager-backend)

# Recipe Manager

The backend API server for management of the ingredients and recipes

## Overview

- Amount unit and Currency management from the admin site
- Ingredient management using API
- Recipe Management using API

## Main Features

- DRF RestAPI
- MySQL
- Swagger API Documentation

## Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone git@github.com/david1992121/recipe-manager-backend.git

Create and activate the virtualenv for your project, install the dependencies:

    $ pip install -r requirements.txt

Create .env file to set the environment variables for the project.

Then apply the migrations and seed the database with initial data:

    $ python manage.py migrate
    $ python manage.py loaddata seed/basics.json

You can also get the mock data for ingrediens and recipes if needed:

    $ python manage.py seed_ingredient 50
    $ python manage.py seed_recipe 30

You can now run the development server:

    $ python manage.py runserver

## API Guide

- Amount unit and currency

The data of the units of amount and currencies can be created and edited in the admin site.
The URL of the admin panel is

```
localhost:8000/admin
```

The data can be only retrieved by the client using the following APIs:

```
/api/v1/basics/amount_units
/api/v1/basics/currencies
```

- Ingredients

The full management of the ingredients data can be allowed from the frontend side using the API.

```
/api/v1/foods/ingredients            - GET, POST
/api/v1/foods/ingredients/{id}       - GET, PUT, PATCH, DELETE
```

- Recipes

The full management of the recipes data can be allowed from the frontend side.

```
/api/v1/foods/recipes                - GET, POST
/api/v1/foods/recipes/{id}           - GET, PUT, PATCH, DELETE
```

When creating a recipe object, the ingredient combination data should be uploaded together.
For example, the payload can be

```
{
    "name": "Carrot Cake",
    "combinations": [
        {
            "ingredient_id": 1,
            "amount": 100
        },
        ...
    ]
}
```

- Swagger API documentation

The detail information can be checked using swagger API documentation on either of the following pages.

```
localhost:8000/redoc
localhost:8000/swagger
```
