# api.tnris.org
Django RESTful API and PostgreSQL backend database management system for maintaining and serving TNRIS's available data and content.

## API and content management system for TNRIS data!
* Check out the wiki to learn about the data model and other curiosities

## Setup

Built with:
* Python 3.6 ([virtual environment](https://howchoo.com/g/nwewzjmzmjc/a-guide-to-python-virtual-environments-with-virtualenvwrapper) suggested)
* PostgreSQL 10.7
  * Amazon RDS Aurora Instance (`tnris-general-store`)
* [Django](https://docs.djangoproject.com/en/3.0/topics/install/)
* For data scripts, you probably want to use some form of python virtual env manager to maintain an isolated environment. A good run-down of the options can be found in [The Hitchiker's Guide to Python](http://docs.python-guide.org/en/latest/dev/virtualenvs/). A recommended setup is virtualenv + virtualenvwrapper.

#### Django App Setup
1. Requires `jq` package to be installed on local os to startup with env variables from SecretsManager: `apt-get update && apt-get install -y jq`
2. Enable your virtual environment. Example: `workon api.tnris.org` (for virtualenv wrapper)
3. Upgrade pip using `pip install --upgrade pip`
4. Install python dependencies:
   * `cd ~/api.tnris.org/src`
   * `pip install -r requirements.txt`
5. Setup secrets files:
   * `./src/data_hub/set-env-secrets.sh`
   * `./src/data_hub/gspread_config.json`
   * **PREFERRED** ::: Place a copy of `vault-password.txt` into the root of this repo `~/api.tnris.org`. Then run `make pull-secrets` to quickly download, decrypt, and properly place both secrets files. *(for TNRIS employees only)*
   * **ALTERNATIVE** ::: A template copy of each secrets file exists in `./src/data_hub/` but with `-example` in the filename. Make a copy of each file in the same directory, remove "-example" from the copy's name, and fill in the values for each secret manually.

## Local Development
1. Set up a local development db instance or use [local port forwarding](https://blog.trackets.com/2014/05/17/ssh-tunnel-local-and-remote-port-forwarding-explained-with-examples.html) to connect to a remote db instance
   * Default settings are already setup if you're using local port forwarding to your port 9000 (skip to next step if you are doing this). If you're using a local development db, configure your database environment variables (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`) to point to it.
2. Since the development of data.tnris.org v2, running the app local now requires installing [GDAL/OGR](https://gdal.org/) on the host. See installation instructions for Debian-based Linux distros here: http://www.sarasafavi.com/installing-gdalogr-on-ubuntu.html
3. `cd ~/api.tnris.org/src/data_hub/`
4. `. set-env-secrets.sh` or `source set-env-secrets.sh` to set the environment variables within the terminal session
5. `python manage.py runserver` to run the app; it will be available at `localhost:8000`. if you get a DB_PASSWORD env variable error then you need to re-run the env variable command in the previous step.

## Deployment Prep

1. `cd ~/api.tnris.org/src`
2. `pip freeze > requirements.txt` to save dependencies
3. `make pull-secrets` if secrets files are not local. they must be locally in `./src/data_hub/` before deploying.
4. save and commit all changes. push to github appropriately.
5. head over to the deployments repo to execute the actual application deployment and make it so

# Lambda

The database API '/areas' endpoint is routinely accessed by a Lambda Function which
pull the resource information and updates the mapserver database table 'areas_view' to join
and host as a map service. This provides an efficient query capability for the Geography map
filter to spatially identify collections.

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
