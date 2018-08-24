# data.tnris.org

![data](https://vignette.wikia.nocookie.net/memoryalpha/images/9/9f/Data_with_pipe.jpg/revision/latest/scale-to-width-down/480?cb=20120823005940&path-prefix=en)

## API and content management system for TNRIS data!
* Check out the wiki to learn about the data model and other curiosities

## Setup

Built with:
* Python 3.6 ([virtual environment](https://howchoo.com/g/nwewzjmzmjc/a-guide-to-python-virtual-environments-with-virtualenvwrapper) suggested)
* PostgreSQL 10.3
  * Amazon RDS Instance
* [Django](https://docs.djangoproject.com/en/2.0/topics/install/)
* For data scripts, you probably want to use some form of python virtual env manager to maintain an isolated environment. A good run-down of the options can be found in [The Hitchiker's Guide to Python](http://docs.python-guide.org/en/latest/dev/virtualenvs/). A recommended setup is virtualenv + virtualenvwrapper.
* Node v10.8.0
* NPM v6.2.0

#### Django App Setup
1. Enable your virtual environment. Example: `workon data.tnris.org` (for virtualenv wrapper)
2. Upgrade pip using `pip install --upgrade pip`
3. Install python dependencies:
   * `cd ~/data.tnris.org/src`
   * `pip install -r requirements.txt`
4. Copy set-env-secrets-example.sh (found in ~/data.tnris.org/src/data_hub/) and rename it set-env-secrets.sh; paste the data.tnris.org RDS pw into the file. * This file is not tracked in version control.
5. Source the set-env-secrets.sh in your virtual environtment using command `source /path/to/your/file/set-env-secrets.sh`
#### React/Node Setup
6. `cd ~/data.tnris.org/src/data_hub/holodeck`
7. `npm install`

## Local Development
1. Set up a local development db instance or use [local port forwarding](https://blog.trackets.com/2014/05/17/ssh-tunnel-local-and-remote-port-forwarding-explained-with-examples.html) to connect to a remote db instance
   * Default settings are already setup if you're using local port forwarding to your port 9000 (skip to next step if you are doing this). If you're using a local development db, configure your database environment variables (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`) to point to it.
2. `cd ~/data.tnris.org/src/data_hub/`
3. **To run the django app locally**: run `python manage.py runserver`, it will be available at `localhost:8000`. if you get a DB_PASSWORD env variable error then you need to re-run the `source` command in 'Setup' step 5 above. Alternatively, run the app locally with `. set-env-secrets.sh && python manage.py runserver` instead as it applies the env variable before startup of the server.
4. **To run the React app locally**: In a separate terminal, `cd ~/data.tnris.org/src/data_hub/holodeck`
5. then `npm start`

## Deployment Prep

<!-- 1. `cd ~/data.tnris.org/src/data_hub`
1. run `python manage.py collectstatic` to compile all static files -->
1. `cd ~/data.tnris.org/src`
1. `pip freeze > requirements.txt` to save dependencies
<!-- 1. `cd ~/data.tnris.org/src/data_hub/holodeck`
1. `npm run build` -->
1. save and commit all changes. push to github appropriately.
1. head over to the deployments repo to execute the actual application deployment and make it so


<!-- ## Notes -->
<!-- * [Django Tutorial](https://docs.djangoproject.com/en/1.11/intro/) -->
