# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

You can check poetry is installed by running `poetry --version` from a terminal.

**Please note that after installing poetry you may need to restart VSCode and any terminals you are running before poetry will be recognised.**

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## MongoDB

The app links to a MongoDB database, to get this running you'll need to log into Azure and create a new CosmosDB instance in your resource group:

- With the Portal:
    - New -> CosmosDB Database
    - Select “Azure Cosmos DB API for MongoDB”
    - Choose “Serverless” for Capacity mode
    - You can also configure secure firewall connections here, but for now you should permit access from “All Networks” to enable easier testing of the integration with the app.
- With the CLI:
    - Create new CosmosDB Account: `az cosmosdb create --name <cosmos_account_name> --resource-group <resource_group_name> --kind MongoDB --capabilities EnableServerless --server-version 4.2`
    - Create new MongoDB database under that account: `az cosmosdb mongodb database create --account-name <cosmos_account_name> --name <database_name> --resource-group <resource_group_name>`
- Update MongoDB environment variables

## Running the App (Locally)

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app 'todo_app/app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 113-666-066
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running the App (Docker)

To run on docker us the following bash commands
```
# Development
docker build --target development --tag todo-app:dev .
docker run -it --env-file ./.env -p 5000:5000 --mount "type=bind,source=$(pwd)/todo_app,target=/app/todo_app" todo-app:dev

# Production
docker build --target production --tag todo-app:prod .  
docker run -it --env-file ./.env -p 5000:5000 todo-app:prod
```

## Running Tests

- Tests are located in the test folder.
- To run all tests, run the command `pytest` from your terminal
- To run all tests in a directory, run `poetry run pytest <<directory>>`
- To run an indiviual test, run the command `pytest -k <<test_name>>` from your terminal or run from vscode > testing
- In Docker:
    - `docker build --target tests --tag todo-app:tests .`
    - `docker run --env-file ./.env.test todo-app:tests`

## Provisioning a VM from an Ansible Control Node

- Set up SSH from the Control to Host(s) ansible node(s)
- Copy/Recreate the files in the ansible folder onto the control node
- Update the necessary values in `.env.j2` and `ansible-inventory`
- Run `ansible-playbook ansible-playbook.yml -i ansible-inventory` to provision

## Azure Hosted App

- Azure container image is hosted at https://hub.docker.com/repository/docker/danielharedevops/todo-app/general
- Application URL: https://todo-app-service.azurewebsites.net/
- To build and push use:
    - `docker build --target production --tag danielharedevops/todo-app .`
    - `docker push danielharedevops/todo-app`
- To push to Azure make a POST request to the webhook link in the Deployment Center of Azure.