# data.tnris.org
![data](https://vignette.wikia.nocookie.net/memoryalpha/images/9/9f/Data_with_pipe.jpg/revision/latest/scale-to-width-down/480?cb=20120823005940&path-prefix=en)
#### API and content management system for TNRIS data

## Setup
Built with:
* Python 3.6 ([virtual environment](https://howchoo.com/g/nwewzjmzmjc/a-guide-to-python-virtual-environments-with-virtualenvwrapper) suggested)
* PostgreSQL 9.6.5
  * Amazon RDS Instance
* [Django](https://docs.djangoproject.com/en/2.0/topics/install/)
* For data scripts, you probably want to use some form of python virtual env manager to maintain an isolated environment. A good run-down of the options can be found in [The Hitchiker's Guide to Python](http://docs.python-guide.org/en/latest/dev/virtualenvs/). A recommended setup is virtualenv + virtualenvwrapper. [Anaconda](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/) is an alternative but it has not been successfully tested.

1. Enable your virtual environment. Example: `workon data-concierge` (for virtualenv wrapper)
2. Upgrade pip using `pip3 install --upgrade pip3`
3. Install python dependencies:
   * `cd ~/tnris-data-concierge/src`
   * `pip3 install -r requirements.txt`

You will need to use your configured AWS CLI when working locally to manage the django static files. If not already set up, you will need to install the AWS CLI and configure it with an access key and secret key.

## Develop

  1. Set up a local development db instance or use [local port forwarding](https://blog.trackets.com/2014/05/17/ssh-tunnel-local-and-remote-port-forwarding-explained-with-examples.html) to connect to a remote db instance
  1. `cd ~/tnris-data-concierge/src/data_concierge`
  1. Configure ~/tnris-data-concierge/src/data_concierge/dev_settings.py to point at your dev db
  1. run `python3 manage.py runserver --settings=data_concierge.dev_settings` to run the app locally and reference prod s3 static files. Will be available at `localhost:8000`

## Deployment Prep

1. Make sure `DEBUG = False` in ~/tnris-data-concierge/src/data_concierge/settings.py
1. `cd ~/tnris-data-concierge/src/data_concierge`
1. run `python3 manage.py collectstatic` to compile all static files and overwrite those in S3. **VERY DANGEROUS** if app is currently deployed as you will be overwriting the production static files!
1. `cd ~/tnris-data-concierge/src`
1. `pip3 freeze > requirements.txt` to save dependencies
1. head over to the deployments repo to execute the actual application deployment


## Notes
* [Django Tutorial](https://docs.djangoproject.com/en/1.11/intro/)
