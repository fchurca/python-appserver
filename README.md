# Python Application Server

| Environment | Build | Coverage|
|--------|-------|---------|
| [Master](https://github.com/fchurca/7552-appserver) | [![Build Status](https://travis-ci.org/fchurca/7552-appserver.svg?branch=master)](https://travis-ci.org/fchurca/7552-appserver)| [![Coverage Status](https://coveralls.io/repos/github/fchurca/7552-appserver/badge.svg)](https://coveralls.io/github/fchurca/7552-appserver)|
| [Stage](https://github.com/adrian-mb/python-appserver) | [![Build Status](https://travis-ci.org/adrian-mb/python-appserver.svg?branch=master)](https://travis-ci.org/adrian-mb/python-appserver) | [![Coverage Status](https://coveralls.io/repos/github/adrian-mb/python-appserver/badge.svg)](https://coveralls.io/github/adrian-mb/python-appserver) |

## Associated Acts
* [Heroku Dashboard](https://dashboard.heroku.com/teams/) (you are logged in, aren't you?)

* Master repositories
    * Android client: [https://github.com/smaraggi/HG-android-client/network]
    * Appserver (this repo): [https://github.com/fchurca/7552-appserver]
    * Shared server: [https://github.com/fchurca/7552-appserver]

* Staging repositories
    * [https://github.com/florrup/sharedserver]
    * [https://github.com/adrian-mb/python-appserver]

## Useful links
* [Subject site](http://7552.fi.uba.ar/)
* [Assignment](https://github.com/taller-de-programacion-2/taller-de-programacion-2.github.io/blob/master/trabajo-practico/enunciados/2017/2/llevame.md)

## Dependencies
For a Docker server on Debian:
https://docs.docker.com/engine/installation/linux/docker-ce/debian/

## Building Docker Image
From the root of the project, where the build scripts are located, execute:
```
appserver$ ./appserver.build.sh
```
This script builds a Docker image from the Dockerfile in the root of the project's tree. The image will be called fiuba/appserver:dev, and this is the name that the execution scripts will later use.

## Deploying Container for Local Development

First create a Docker network for Mongo and server containers:
```
appserver$ docker network create taller
```

Launch now a MongoDB container:
```
appserver$ ./mongo.run.sh
```
After Mongo is up, run in another terminal:
```
appserver$ ./appserver.run.sh
```
The script launches the image fiuba/appserver:dev inside a container. The container is configured as follows:

* Port 8080 of the container is mapped to port 8080 of the host.

* Container is placed inside network `taller`, with name `appserver.taller`.

* The project's source code directory in the host is mapped to the directory where gunicorn looks for the application scripts. Since gunicorn is executed with live reload, local live edits to the application code will be instantly reloaded by gunicorn without having to build the image and reload the container once again.

## Deploying to Heroku

To deploy to Heroku simply push the contents of the source directory into the Heroku repository. Before deploying, however, the following environment variables need to be set:

* `APPSERVER_CFG`: directory where the configuration files are located, relative to the root of the project.

* The variable that defines the connection string to some MongoDB instance. The name of this variable must be defined in the file `mongo.ini` inside the configuration directory:
```
[Connection]
mongovar=MONGODB_URI
database=db
```
Then, in this case, the connection string is equal to the value of the variable MONGODB_URI. Alternatively, the connection string can be placed directly inside the configuration file as follows:
```
[Connection]
uri=<connection string>
database=db
```
For security reasons, however, this may not be desirable.

## Building Redistributable Package

First install Python dependency setuptools:
```
appserver$ pip install setuptools
```
Then execute from the root of the project directory
```
appserver$ python setup.py sdist
```
This should generate a redistributable archive file under a newly created dist directory. 

## Installing and Executing Redistributable Package
To install the package, execute
```
$ pip install <path to archive file>
```
Application server can then be executed using gunicorn:
```
$ pip install gunicorn
$ gunicorn --workers 4 appserver:app
```

## Generating Doxygen Documentation
```
appserver$ apt-get install doxygen graphviz
appserver$ doxygen
```
HTML documentation will be placed inside the docs/generated directory.

## Troubleshooting

### Mongo complains about `No space left on device: "/data/db/journal"`

Dangling old volumes may still be laying around
```
# list
docker volume ls -qf dangling=true
# remove
docker volume rm $(docker volume ls -qf dangling=true)
```
