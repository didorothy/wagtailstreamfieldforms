Development
===========

Useful getting started instructions for making code modifications.


How to run the Test Suite:

.. code-block:: bash

    export DJANGO_SETTINGS_MODULE=tests.settings
    coverage run manage.py test


How to run the example site:

.. code-block:: bash

    export DJANGO_SETTINGS_MODULE=example.settings
    python manage.py runserver

How to use tox:

.. code-block:: bash

    pip install tox
    tox

**NOTE:** tox may not work yet. Please test and then update this page.