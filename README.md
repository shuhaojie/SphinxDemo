# Tutorial

Brief tutorial of sphinx on how to build quick api documentation.

## install sphinx

```
pip install sphinx
```

if you are python3

```
pip3 install sphinx
```

## create a project

create a project which contains `docs` and `src` folders

```bash
+-- docs
+-- src
| +--demo1.py
| +--demo2.py
```

## build API documentation

### create sphinx environment

```
cd docs

sphinx-quickstart
```

Choose the default as your sphinx configuration. After this step, your `docs` folder will be like

```bash
+-- docs
| +--\_build
| +--\_static
| +--\_templates
| +--conf.py
| +--index.rst
| +--make.bat
| +--Makefile
```

### configure your sphinx

Go to `conf.py` to add the path of `src`

```
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
```

Also, in your extensions, add the follows

```
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.napoleon'
              ]
```

Finally, edit your `index.rst` to build API documentation.

```
Welcome to Sphinx Demo's documentation!
=======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

src demo1
===================
.. automodule:: src.demo1
   :members:

src demo2
=====================
.. automodule:: src.demo2
   :members:
```

### create rst files

Go back to your project and type `sphinx-apidoc -f -o source src`, you will have three `.rst` files.

```bash
+-- project
| +-- docs
| +-- source
    | +--demo1.rst
    | +--demo2.rst
    | +--modules.rst
| +-- src
    | +--demo1.py
    | +--demo2.py
```

### crate the HTML or PDF files

For html, you type `make html` in `docs` dictionary. Make sure this step doesn't have any warnings or errors so that your build is successful. Go to `docs/_build/html/index.html` to see your documentation.

# References

1. <https://blog.csdn.net/sinat_29957455/article/details/83657029>
2. <https://www.w3xue.com/exp/article/20201/72756.html>
3. <https://stackoverflow.com/questions/10324393/sphinx-build-fail-autodoc-cant-import-find-module>
4. <https://medium.com/better-programming/auto-documenting-a-python-project-using-sphinx-8878f9ddc6e9>
