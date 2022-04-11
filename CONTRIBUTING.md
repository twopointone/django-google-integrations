# Contributing
All contributions are much welcome and greatly appreciated! Expect to be credited for you effort.

## General
Generally try to limit the scope of any Pull Request to an atomic update if possible. This way, it's much easier to assess and review your changes.

You should expect a considerably faster turn around if you submit two or more PRs instead of baking them all into one major PR.


## Coding conventions

- Read and pay attention to current code in the repository
- For the Python part, we follow pep8 in most cases. We use [flake8][flake8] to check for linting errors. Once you're ready to commit changes, check your code with `flake8`.
- Install a plugin for [EditorConfig][editorconfig] and let it handle some of the formating issues for you.
- For the Django part, we follow standard [Django coding style][django-coding style].
- And always remember the Zen.

[editorconfig]: http://editorconfig.org/
[flake8]: http://flake8.readthedocs.org/en/latest/
[django-coding style]: https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/coding-style/


## Get Started!

1. Fork the django-google-integrations repo on GitHub.

2. Clone your fork locally:

`$ git clone git@github.com:PrimedigitalGlobal/django-google-integration.git`


3. Install Virtual env

```
pip install virtualenv
pip install virtualenvwrapper
```

4. Source virtualenv wrapper in bash profile and then create a new virtual env for django_google_integrations

```
vim ~/.bash_profile
source /usr/local/bin/virtualenvwrapper.sh

# save the file and source bash profile
source ~/.bash_profile

mkvirtualenv django_google_integrations -p python3
```

5. Once a virtualenv is created you can switch to that using

```
workon django_google_integrations
```

6. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development:
```
$ cd django-google-integration
$ python setup.py develop
```

7. Once you have created/activated virtual environment. Install all the python requirements

```
pip install -U -r requirements/development.txt
```

8. Install pre-commit

```
pre-commit install
```

9. Create a branch for local development:
```
git checkout -b name-of-your-bugfix-or-feature
```

10. Once you are done making changes, run tox to test your code.
```
$ tox
```

11. Commit your changes and push your branch to GitHub:
```
git add .
git commit -m "Your detailed description of your changes."
git push origin name-of-your-bugfix-or-feature
```

12. Submit a pull request through the GitHub website.

13. Start local server and visit localhost:8000

```
python manage.py migrate
python manage.py runserver
```

## Pull Request Guidelines
Before you submit a pull request, check that it meets these guidelines:

1. All the pull requests are made against `master` branch.

2. The pull request should include tests.

3. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring, and add the feature to the list in README.md.
