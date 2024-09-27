# Switchdin Middleware

## Developed by: Divakar Patil <divakarpatil35@gmail.com>

## Application Background

A middleware which sits between DER and Network operator.
It allows DER to register themselves with the Network Operator
which gives the Network Operator visibility of the DER so it can send Export
Limits to the DER. These Export Limits are to ensure that DER does not export
too much power to the grid and enable the Network Operator to maintain stability
in the electricity grid.

## Prerequisites

1. Python 3.10

## Application ERD

Application Database Entity Relation Diagram can be found [here](docs/database_modeling.png)

## Application Tech Stack

1. Python
2. Fastapi
3. Postgres
4. Redis
5. Celery

### Commands

Follow below commands to setup and run application on your local:

- Create venv and install project dependencies

    ```bash
    make install-dependencies
    ```

- Create .env file from .env.example

    ```bash
    cp .env.example .env
    ```

- Start Celery worker

    ```bash
    make start-celery
    ```

- Start application

    ```bash
    make start-app
    ```

- Open browser and paste below link.

    ```bash
    http://127.0.0.1:8000/docs
    ```

- Run Tests.

    ```bash
    make tests
    ```

## APIs

1. [Energy resource registration API flow](docs/energy_resource_registration_api_flow.png)
2. [Site export limit update API flow](docs/update_export_limit_api_flow.png)
3. [Energy resource export limit fetch API flow](docs/energy_resource_export_limit_api_flow.png)
4. [Energy resource meter reading API flow](docs/energy_resource_meter_reading_api_flow.png)
