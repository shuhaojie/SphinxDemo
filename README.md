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

create a `src` folder which contaions two `.py` files

```bash
+--root
|   +-- src
    | +--demo1.py
    | +--demo2.py
```

## Build API documentation

### Create sphinx environment

In your `root` dictionary

```
sphinx-quickstart
```

Choose the default as your sphinx configuration. After this step, your `root` folder will be like

```bash
+-- root
| +--src
| +--\_build
| +--\_static
| +--\_templates
| +--conf.py
| +--index.rst
| +--make.bat
| +--Makefile
```

### Configure your sphinx

Go to `conf.py` to add the path of `src`

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
html_theme = 'classic'
```

### Create rst files

Go back to your project and type `sphinx-apidoc -f -o source src`, you will have three `.rst` files.

```bash
+-- project
| +-- source
    | +--demo1.rst
    | +--demo2.rst
    | +--modules.rst
| +-- src
    | +--demo1.py
    | +--demo2.py
```

edit your `deom1.rst` file as follow

```
src.demo1
============

.. automodule:: src.demo1
   :members:
   :undoc-members:
   :show-inheritance:
```

`deom2.rst` is the same

### Edit index.rst

Finally, edit your `index.rst` to build API documentation.

```
Welcome to Sphinx Demo's documentation!
=======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   source/demo1
   source/demo2

### Create the HTML or PDF files

For html, you type `make html` in `root` dictionary. Make sure this step doesn't have any warnings or errors so that your build is successful. Go to `/_build/html/index.html` to see your documentation.

# References

1. <https://blog.csdn.net/sinat_29957455/article/details/83657029>
2. <https://www.w3xue.com/exp/article/20201/72756.html>
3. <https://stackoverflow.com/questions/10324393/sphinx-build-fail-autodoc-cant-import-find-module>
4. <https://medium.com/better-programming/auto-documenting-a-python-project-using-sphinx-8878f9ddc6e9>
```
