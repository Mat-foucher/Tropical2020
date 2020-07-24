.. _dev-install:

Installation for Developers
===========================

This guide will show you how to install the project using the command line.

This project uses `Sphinx <https://www.sphinx-doc.org/en/master/>`_ to automatically generate documentation from
`Numpy docstrings <https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard>`_
(examples can be found `here <https://www.sphinx-doc.org/en/master/usage/extensions/example_numpy.html>`_).
This documentation
is used by `GitHub Pages <https://pages.github.com/>`_ to host the documentation you're reading right now. For this
reason, the generated documentation is kept in its dedicated ``gh-pages`` branch.

First create a directory to hold the project and enter it:

.. code-block:: none

    mkdir project
    cd project

Then clone the repository where you will edit the project source code:

.. code-block:: none

    git clone https://github.com/cmeredit/Tropical2020.git

Setting up the docs repository is slightly more complex:

.. code-block:: none

    mkdir Tropical2020-docs
    cd Tropical2020-docs
    git clone https://github.com/cmeredit/Tropical2020.git html
    cd html
    git checkout -b gh-pages remotes/origin/gh-pages

At this point, ``project/Tropical2020`` contains the source code for the project, while ``project/Tropical2020-docs``
contains the automatically generated documentation used by GitHub Pages.

Next, we will create a `virtual environment <https://docs.python.org/3/tutorial/venv.html>`_ that will be used while
developing. From ``project/Tropical2020``, create and activate a virtual environment:

.. code-block:: none

    python3 -m venv env
    source env/bin/activate

The project uses `pytest <https://docs.pytest.org/en/stable/>`_ for its testing and
`Sphinx <https://www.sphinx-doc.org/en/master/>`_ for its documentation, so we will install those:

.. code-block:: none

    pip3 install pytest
    pip3 install sphinx

Finally, install the package in editable mode:

.. code-block:: none

    pip3 install -e .

To verify that everything has been installed correctly, you can run ``pytest`` from ``project/Tropical2020``. This will
produce a lot of text output, but you should see at the bottom of the output that all tests ran successfully. To
deactivate the virtual environment, simply run ``deactivate``.

The project is now installed. To start working on it, read the guide about :ref:`contributing`.
