.. _contributing:

Contributing to the Project
===========================

This contribution guide assumes that the project is installed as described in :ref:`dev-install`. Here are some
guidelines for contributing to the project.

- Do not commit directly to the master branch.
- Write short commit messages in the imperative mood. See `this post <https://chris.beams.io/posts/git-commit/>`_ for
  more details.
- Comment your code.
- Write docstrings for your code.
- Write tests for your code in ``project/Tropical2020/test``.
- To add a new feature ``your_feature`` to a branch ``base_branch``, take the following steps:
    1. Set up your development branch:
        1. Checkout the base branch with ``git checkout base_branch``.
        2. Make a branch named after your feature and check it out with ``git checkout -b your_feature``.
    2. Add your features. Once the code is stable, commented, and includes docstrings, and once all of your tests are
       written and pass, continue to the next step.
    3. If ``base_branch`` is ``master``, then rebuild the documentation:
        1. From ``project/Tropical2020/docs``, run ``sphinx-apidoc --separate -f -o source ../Tropical2020`` followed
           by ``make html``. This will generate the project documentation in ``project/Tropical2020-docs/html``.
        2. Open ``project/Tropical2020-docs/html/index.html`` and make sure the parts of the documentation relating to
           your changes are correct.
    4. Merge your feature branch into ``base_branch``.
    5. If ``base_branch`` is ``master``, then navigate to ``project/Tropical2020-docs/html``, add and commit any
       changes, and push to ``gh-pages``.
  Congratulations! Your feature is now part of ``base_branch``! If ``base_branch`` was ``master``, then your changes
  are now also reflected in the project documentation.
