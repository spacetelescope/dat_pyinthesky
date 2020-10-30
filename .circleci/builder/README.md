# dat_pyinthesky Readme

## Setting up dat_pyinthesky build environment

`dat_pyinthesky` assumes it can be ran in a docker container. You'll find this container in listed in `.circleci/config.yaml` 
under `executors.notebook-executor.docker.image`. There are some additional modifications ran against the container to create a
more complient image for the python codes to run in. You'll find these in the `Setup Environment` section of each Job

The following snippet is meant to show to to setup the environment on a local machine

```
$ sudo apt-get update
$ sudo apt-get install -y python-virutalenv curl build-essential gcc-4.8
$ git clone git@github.com:spacetelescope/dat_pyinthesky.git
$ cd dat_pyinthesky
$ virtualenv -p $(which python3) venv
$ source venv/bin/activate
$ pip install -U pip jupyterlab
$ pip install -U https://github.com/eteq/nbpages.git@b9ec8410803357939210e068af7e14a6f0625fab#egg=nbpages
```

## Building asdf_example into html

`dat_pyinthesky` Build Machinery has multiple modes, we'll focus only on `build-notebooks` and `build-website`. In `build-notebooks`, there is -c and -n for collection and category.
It'll build only one category of the collection using jupyterlab nbconvert and render an HTML artifact somewhere in the filesystem

```
$ source venv/bin/activate
$ python ./.circleci/builder/factory.py -o build-notebooks -c jdat_notebooks -n asdf_example
$ python ./.circleci/builder/factory.py -o build-website -c jdat_notebooks -n asdf_example
```

