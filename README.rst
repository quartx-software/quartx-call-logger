.. image:: https://api.codacy.com/project/badge/Grade/af3dc404e10e4a8f9f8e79823ff654e9
    :target: https://www.codacy.com/app/Quartx/quartx-call-logger?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=quartx-software/quartx-call-logger&amp;utm_campaign=Badge_Grade

.. image:: https://travis-ci.org/quartx-software/quartx-call-logger.svg?branch=master
    :target: https://travis-ci.org/quartx-software/quartx-call-logger

.. image:: https://coveralls.io/repos/github/quartx-software/quartx-call-logger/badge.svg?branch=master
    :target: https://coveralls.io/github/quartx-software/quartx-call-logger?branch=master

.. image:: https://readthedocs.org/projects/quartx-call-logger/badge/?version=latest
    :target: https://quartx-call-logger.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


Quartx Call Logger
------------------

Call logger component for the Quartx phone system monitoring frontend. https://quartx.ie/

This logger can monitor phone systems for CDR(Call Data Records) and send the records to the monitoring frontend.
The monitoring frontend will then analyze the records and display them in a easy to view web interface.

The currently supported phone systems are:

    * Siemens Hipath

Support for new phone systems can be easily added through plugins.
With the plugin system any system can be supported as long as the system has some sort of API or Serial Interface.
The documentation on how to create a plugin can be found here.
https://quartx-call-logger.readthedocs.io/en/latest/?badge=latest.


Install
-------

Currently only install from git repo is supported, but PyPI support will be added later.

Dependencies ::
    
    sudo apt-get install python3-pip git

Production ::

    sudo pip3 install git+https://github.com/quartx-software/quartx-call-logger.git

Development ::

    git clone https://github.com/quartx-software/quartx-call-logger.git
    cd quartx-call-logger
    pip install pipenv
    pipenv install --dev


Configuration
-------------

The Configuration for this package is located in ``/Library/Application Support/quartx`` on MacOS,
``/etc/xdg/quartx`` on Unix/Linux or ``C:\ProgramData\quartx\quartx`` on Windows.

First we download the base configuration file from github so we can modifiy it. The following commands are for Linux/Unix.
::

    sudo mkdir -p /etc/xdg/quartx
    sudo curl https://raw.githubusercontent.com/quartx-software/quartx-call-logger/master/data/call-logger.yml > call-logger.yml
    sudo cp call-logger.yml /etc/xdg/quartx/call-logger.yml
    

Currently the only required settings is the ``token``. The token is the authentication key used to authenticate
the user and identify who the call logs belong to. Contact Quartx Call Monitoring for the token key.
::

    sudo nano /etc/xdg/quartx/call-logger.yml
    ...
    token: bd6a567386f79329b156a042a1aac9f44726e736
    ...

The plugin settings may also need to be changed depending on the phone system.
You can read the configuration comments to see what changes may be required.


Usage
-----

The call logger can be run with just one single command when on Linux.
::

    call-logger

To run the call-logger as a service you can install the systemd service file
::

    sudo curl https://raw.githubusercontent.com/quartx-software/quartx-call-logger/master/data/quartx-call-logger.service > call-logger.service
    sudo cp call-logger.service /etc/systemd/system/call-logger.service
    sudo systemctl enable --now call-logger.service


Contribution
------------

Support for other phone systems can be added through plugins.
Documentation for creating plugins can be found at readthedocs.
https://quartx-call-logger.readthedocs.io/en/latest/?badge=latest.
