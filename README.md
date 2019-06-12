# api.tnris.org
Django RESTful API and PostgreSQL backend database management system for maintaining and serving TNRIS's available data and content.

## API and content management system for TNRIS data!
* Check out the wiki to learn about the data model and other curiosities

## Setup

Built with:
* Python 3.6 ([virtual environment](https://howchoo.com/g/nwewzjmzmjc/a-guide-to-python-virtual-environments-with-virtualenvwrapper) suggested)
* PostgreSQL 10.3
  * Amazon RDS Instance
* [Django](https://docs.djangoproject.com/en/2.0/topics/install/)
* For data scripts, you probably want to use some form of python virtual env manager to maintain an isolated environment. A good run-down of the options can be found in [The Hitchiker's Guide to Python](http://docs.python-guide.org/en/latest/dev/virtualenvs/). A recommended setup is virtualenv + virtualenvwrapper.

#### Django App Setup
1. Enable your virtual environment. Example: `workon api.tnris.org` (for virtualenv wrapper)
2. Upgrade pip using `pip install --upgrade pip`
3. Install python dependencies:
   * `cd ~/api.tnris.org/src`
   * `pip install -r requirements.txt`
4. Copy set-env-secrets-example.sh (found in ~/api.tnris.org/src/data_hub/) and rename it set-env-secrets.sh; paste the data.tnris.org RDS pw into the file. * This file is not tracked in version control. **--or--** place a copy of `vault-password.txt` into the root of this repo `~/api.tnris.org`. You might need to change spaces to newlines. cd into the root folder and run `make pull-secrets` to quickly download, decrypt, and properly place the secrets file.
5. Source the set-env-secrets.sh in your virtual environtment using command `source /path/to/your/file/set-env-secrets.sh`

## Local Development
1. Set up a local development db instance or use [local port forwarding](https://blog.trackets.com/2014/05/17/ssh-tunnel-local-and-remote-port-forwarding-explained-with-examples.html) to connect to a remote db instance
   * Default settings are already setup if you're using local port forwarding to your port 9000 (skip to next step if you are doing this). If you're using a local development db, configure your database environment variables (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`) to point to it.
2. `cd ~/api.tnris.org/src/data_hub/`
3. **To run the django app locally**: run `python manage.py runserver`, it will be available at `localhost:8000`. if you get a DB_PASSWORD env variable error then you need to re-run the `source` command in 'Setup' step 5 above. Alternatively, run the app locally with `. set-env-secrets.sh && python manage.py runserver` instead as it applies the env variable before startup of the server.

## Deployment Prep

1. `cd ~/api.tnris.org/src`
1. `pip freeze > requirements.txt` to save dependencies
1. save and commit all changes. push to github appropriately.
1. head over to the deployments repo to execute the actual application deployment and make it so

# Lambda

The database API '/areas' endpoint is routinely accessed by a Lambda Function which
creates a CSV and dumps it into S3 for Carto to sync with. This provides an efficient
query capability for the Geography map filter to spatially identify collections directly
in Carto.

### Lambda Development
1. make a new python virtual environment (separate from the app's above) for lambda development. This is required as all associated python packages will need to be bundled
for deployment and we don't want un-needed packages included.
2. enable the lambda function's virtual environment. Example: `workon lambda-areas_view` (for virtualenv wrapper)
3. Upgrade pip using `pip install --upgrade pip`
4. Install python dependencies (example):
   * `cd ~/api.tnris.org/lambda-areas_view`
   * `pip install -r requirements.txt`
5. run the function with `python lambda_function.py` (will need the aws cli set up with proper permissions)

### Lambda Deployment Prep
1. go through the development steps and run the function locally to ensure it is running as expected
2. enable the lambda function's virtual environment. Example: `workon lambda-areas_view` (for virtualenv wrapper)
3. cd into the repo root with `cd ~/api.tnris.org`
4. run `make pack-lambda-areas_view` (example) to copy the python dependencies from the virtual env into the lambda function folder
5. hop over to the tnris deployments repo to run the rest
