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
   * **PREFERRED** ::: Place a copy of `vault-password.txt` into the root of this repo `~/api.tnris.org`. Then run `make pull-secrets` to quickly download, decrypt, and properly place both secrets files. (requires ansible-vault to be installed) *(for TNRIS employees only)* 
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
3. save and commit all changes.
4. push to github master branch to fire off the ci/cd pipeline which will automatically build and deploy to the staging env for review, and upon manual approval, then to the production env

## Tests

deployment tests located in the ./tests/ directory

* `endpoint_tests.sh` runs within CodeBuild during deployment to validate api rest endpoints and landing pages are returning proper response codes before manual review & approval. must set variable `domain` when calling; example: `domain=stagingapi.tnris.org . ./tests/endpoint_tests.sh`

## Notes

* The database API '/areas' endpoint is routinely accessed by a Lambda Function which
pull the resource information and updates the mapserver database table 'areas_view' to join
and host as a map service. This provides an efficient query capability for the Geography map
filter to spatially identify collections.
