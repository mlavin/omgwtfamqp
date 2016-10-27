OMGWTFAQMP
==========

This is a demo application which pairs with a talk I've given on AMQP. As such there is no real
ongoing maintaince of this project. You are welcome to use this code within the terms of the
license but please do not expect any kind of support or future updates.


Installing the Requirements
---------------------------

This requires Python 3.5 and the additional requirements are listed in the ``requirements.txt`` file::

    $ mkvirtualenv omgwtfamqp -p `which python3.5`
    (omgwtfamqp) $ pip install -r requirements.txt

The application assumes that you are running RabbitMQ on the default port and accessible on localhost.
It also assumes that the default ``guest`` user can connect. You should refer the directions for
installing RabbitMQ on your OS of choice.


Running the Demo
----------------

With the virtualenv activated and the requirements all installed you can run the web application via::

    (omgwtfamqp) $ python app.py

This will start the web application on port 8080. You also need to run one or more task workers
which can be started via::

    (omgwtfamqp) $ python worker.py

Browsing to http://localhost:8080/demo.html will display the live update worker stream. To trigger
a webhook and see all of the pieces working together you can POST to the running webserver with 
``curl``::

    $ curl -X POST -d project=omg -d user=mlavin http://localhost:8080/

Both the ``project`` and ``user`` keys are required in the POST.


License
-------

This code is made available under the BSD license. You are free to use, modify, and redistribute
it within those terms.
