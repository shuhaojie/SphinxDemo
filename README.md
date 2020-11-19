# Tutorial

Brief tutorial of sphinx on how to build quick api documentation.

## Install sphinx

```
pip install sphinx
```

if you are python3

```
pip3 install sphinx
```

## Create a project

Project contaions three folders: `demo`, `tensorgraph`, `examples`

```bash
+--root
|   +-- demo
    | +--demo1.py
    | +--demo2.py
|   +-- tensorgraph
    | +--dataset
    | +--layers
    | +--models_zoo
    | +--cost.py
    | +--...
|   +-- examples
    | +--example.py
    | +--...

```

## Build API documentation

### Create sphinx environment

In your `root` dictionary

```
sphinx-quickstart
```

Choose default and answer the question. After this step, your `root` folder will be like

```bash
+-- root
| +--demo
| +--tensorgraph
| +--examples
| +--\_build
| +--\_static
| +--\_templates
| +--conf.py
| +--index.rst
| +--make.bat
| +--Makefile
```

### Configure your sphinx

Go to `conf.py` to make three folders in the path

```
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
```

Also, in your extensions, add the follows

```
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.napoleon'
              ]
```

Change the theme if you like

```
html_theme = 'nature'
```

### Create rst files

In your `root` dictionary, type `mkdir source` to new a folder. Then type the follows

```
sphinx-apidoc -f -o source/demo demo
sphinx-apidoc -f -o source/tensorgraph tensorgraph
sphinx-apidoc -f -o source/examples examples
```

you `source` folder will be like:

```bash
+-- source
| +-- demo
    | +--demo1.rst
    | +--demo2.rst
    | +--modules.rst
| +-- examples
    | +--example.rst
    | +--...
    | +--...modules.rst
| +-- tensorgraph
    | +--tensorgraph.rst
    | +--...
    | +--...modules.rst
```

### Edit index.rst

Finally, edit your `index.rst` to build API documentation.

```
Welcome to Sphinx Demo's documentation!
=======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   source/demo/modules
   source/examples/modules
   source/tensorgraph/modules
```

Take `tensorgraph` as example. The `modules.rst` file is like

```
tensorgraph
===========

.. toctree::
   :maxdepth: 4

   tensorgraph
```

This shows that `modules.rst` directs to `tensorgraph.rst` which is like as follow

```
tensorgraph
===================

dataset
-----------------------

.. toctree::
   :maxdepth: 4

   tensorgraph.dataset

layers
-----------

.. toctree::
   :maxdepth: 4

   tensorgraph.layers

models_zoo
-----------

.. toctree::
   :maxdepth: 4

   tensorgraph.models_zoo

cost
-----------------------

.. automodule:: tensorgraph.cost
   :members:
   :undoc-members:
   :show-inheritance:

data\_iterator
---------------------------------

.. automodule:: tensorgraph.data_iterator
   :members:
   :undoc-members:
   :show-inheritance:

graph
------------------------

.. automodule:: tensorgraph.graph
   :members:
   :undoc-members:
   :show-inheritance:

node
-----------------------

.. automodule:: tensorgraph.node
   :members:
   :undoc-members:
   :show-inheritance:

progbar
--------------------------

.. automodule:: tensorgraph.progbar
   :members:
   :undoc-members:
   :show-inheritance:

sequential
-----------------------------

.. automodule:: tensorgraph.sequential
   :members:
   :undoc-members:
   :show-inheritance:

stopper
--------------------------

.. automodule:: tensorgraph.stopper
   :members:
   :undoc-members:
   :show-inheritance:

trainobject
------------------------------

.. automodule:: tensorgraph.trainobject
   :members:
   :undoc-members:
   :show-inheritance:

utils
------------------------

.. automodule:: tensorgraph.utils
   :members:
   :undoc-members:
   :show-inheritance:

```

For `tensorgraph.dataset`, it will direct to `tensorgraph.dataset.rst`, as follow

```
cifar10
----------------------------------

.. automodule:: tensorgraph.dataset.cifar10
   :members:
   :undoc-members:
   :show-inheritance:

cifar100
-----------------------------------

.. automodule:: tensorgraph.dataset.cifar100
   :members:
   :undoc-members:
   :show-inheritance:

mnist
--------------------------------

.. automodule:: tensorgraph.dataset.mnist
   :members:
   :undoc-members:
   :show-inheritance:

preprocess
-------------------------------------

.. automodule:: tensorgraph.dataset.preprocess
   :members:
   :undoc-members:
   :show-inheritance:

```

All contents in tensorgraph.dataset are moduls, so there will be no directs any more.

### Create the HTML or PDF files

For html, you type `make html` in `root` dictionary. Make sure this step doesn't have any warnings or errors so that your build is successful. Go to `/_build/html/index.html` to see your documentation.

# References

1. <https://blog.csdn.net/sinat_29957455/article/details/83657029>
2. <https://www.w3xue.com/exp/article/20201/72756.html>
3. <https://stackoverflow.com/questions/10324393/sphinx-build-fail-autodoc-cant-import-find-module>
4. <https://medium.com/better-programming/auto-documenting-a-python-project-using-sphinx-8878f9ddc6e9>
