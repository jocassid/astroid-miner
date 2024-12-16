# astroid-miner
Wrapper around the [astroid](https://pypi.org/project/astroid/) library to aid 
in static code analysis.  I'm planning on using the astroid library to parse 
Python source files and navigate class and function definitions.  Here's the
features that I'm working on implementing:

## Generic Code Analysis

* call_diagram: Given a target function or method, find the 
functions/methods called by and/or lead to the target being called.
* show_path: Display the PYTHONPATH based on `sys.path` and path append or 
substitute command line arguments

## Django-specific features (these will be moved into separate package)

* url_to_view: Given a url in a django project identify the class or function
providing the view and identify the file and line number where that view is 
defined.

