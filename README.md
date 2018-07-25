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
* For data scripts, you probably want to use some form of python virtual env manager to maintain an isolated environment. A good run-down of the options can be found in [The Hitchiker's Guide to Python](http://docs.python-guide.org/en/latest/dev/virtualenvs/). A recommended setup is virtualenv + virtualenvwrapper. [Anaconda](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/) is an alternative but it has not been successfully tested.

1. Enable your virtual environment. Example: `workon data.tnris.org` (for virtualenv wrapper)
2. Upgrade pip using `pip install --upgrade pip`
3. Install python dependencies:
   * `cd ~/data.tnris.org/src`
   * `pip install -r requirements.txt`
4. Copy set-env-secrets-example.sh and rename it set-env-secrets.sh; paste the data.tnris.org RDS pw into the file. * This file is not tracked in version control.
5. Source the set-env-secrets.sh in your virtual environtment using command `source /src/to/your/file.sh`
1. Set up a local development db instance or use [local port forwarding](https://blog.trackets.com/2014/05/17/ssh-tunnel-local-and-remote-port-forwarding-explained-with-examples.html) to connect to a remote db instance
1. `cd ~/data.tnris.org/src/data-hub`
1. Configure ~/data.tnris.org/src/data-hub/dev_settings.py to point at your dev db
1. run `python manage.py runserver --settings=data-hub.dev_settings` to run the app locally, it will be available at `localhost:8000`

## Deployment Prep

### Note: A deployment for this app has yet to be created

1. Make sure `DEBUG = False` in ~/data.tnris.org/src/data-hub/settings.py
1. `cd ~/data.tnris.org/src/data-hub`
1. run `python manage.py collectstatic` to compile all static files
1. `cd ~/data.tnris.org/src`
1. `pip freeze > requirements.txt` to save dependencies
1. head over to the deployments repo to execute the actual application deployment and make it so


## Notes
* [Django Tutorial](https://docs.djangoproject.com/en/1.11/intro/)
