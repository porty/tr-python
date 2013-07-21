Total Recall in Python
======================

What is this?
-------------

This is a solution to http://totalrecall.99cluster.com/ , written in Python.
It's non-interactive: you watch it play the game (and win). This is just to
show that a solution can be written in python.

How to run?
-----------

<pre>
python main.py
</pre>
Or:
<pre>
./main.py
</pre>

What are the other files?
-------------------------

backend.py

* Backends to run the game against - currently just a REST-based backend

rest.py

* A simple class for REST-based interfaces

settings.py

* Settings for the application (REST server to use, name/email to post)

solver.py

* Solvers to solve a given Total Recall game

test.py

* Unit testing - go ahead and run it!
