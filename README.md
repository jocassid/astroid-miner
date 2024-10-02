# astroid-miner
Wrapper around the [astroid](https://pypi.org/project/astroid/) library to aid 
in static code analysis.  I'm planning on using the astroid library to parse 
Python source files and navigate class and function definitions.  Here's the
features that I'm working on implementing:

* call_diagram: Given a target function or method, find the 
functions/methods called by and/or lead to the target being called.
* url_to_view: Given a url in a django project identify the class or function
providing the view and identify the file and line number where that view is 
defined.

