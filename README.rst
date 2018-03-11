.. image:: https://img.shields.io/readthedocs/xcbv.svg?style=for-the-badge
   :target: https://xcbv.readthedocs.io
.. image:: https://img.shields.io/circleci/project/github/yourlabs/xcbv/master.svg?style=for-the-badge
   :target: https://circleci.com/gh/yourlabs/xcbv
.. image:: https://img.shields.io/codecov/c/github/yourlabs/xcbv/master.svg?style=for-the-badge
   :target: https://codecov.io/gh/yourlabs/xcbv
.. image:: https://img.shields.io/npm/v/xcbv.svg?style=for-the-badge
   :target: https://www.npmjs.com/package/xcbv
.. image:: https://img.shields.io/pypi/v/xcbv.svg?style=for-the-badge
   :target: https://pypi.python.org/pypi/xcbv

What it is
==========

- remove need of urls.py in favor of nested views,
- nested security checking support,
- takes DRY to another level with view route parenting,
- django can you generate a menu is: yes,
- modern pattern for creating your own admin-like CRUD,

Extracted from CRUDLFA+, re DDD'd, under TDD.

.. code-block:: python

    # yourapp.views
    urlpatterns = xcbv.Router(
        xcbv.TemplateView.factory(
            name='index', # default /index to index.html
        ),
        YourOtherView,
        xcbv.Router(
            YourListView.factory(
                # by default only staff sees new views, this opens for all
                allows=lambda self: True
            ),
            YourUpdateView.factory(
                # could be set here or inside the view
                path='specialupdate/<slug0>/<slug1>',
            ),
            ObjectFormView.factory(
                form_class=YourCustomForm
                key='custom',
            ),
            YourDetailView.factory(
                # just adding a sub object list view inside URL and
                # permission tree like a Poney, is this going to be a
                # list of child models from the above ModelView model ?
                views=xcbv.ListView(
                    model=YourChildModel,
                )
            )
            # the above should replace CRUD views defined in setting
            # XCBV['MODELVIEW_DEFAULT_CHILDREN'] and add object action
            # "custom"
            model=YourModel,
            menus=('global', 'footer'),
            icon="fa-love",
        ),
        # Router always takes a namespace or class (ie. model) arg
        namespace='yourapp',
    ).urlpatterns()

    # yourproject.urls
    urlpatterns += path('yourmodel/', yourapp.views.router.urlpatterns())

    # in templates
    # menu for navigation
    {% for view in |views_in_menu:''|views_allowing:request %}
      <a
        href={{ view.absolute_url }}
        title={{ view.title }}
      ><span class="fa-icon {{ view.fa_icon }}"></span>
    {% endfor %}

    # menu for model
    {% for view in self|views_in_menu:'model'|views_allowing:request %}
      <a
        href={{ view.absolute_url }}
        title={{ view.title }}
      ><span class="fa-icon {{ view.fa_icon }}"></span>
    {% endfor %}

    # menu for object
    {% for view in self|views_in_menu:'object'|views_allowing:request %}
      <a
        href={{ view.absolute_url }}
        title={{ view.title }}
      ><span class="fa-icon {{ view.fa_icon }}"></span>
    {% endfor %}

Demo
====

Run the demo which uses Django server side::

    pip install --user xcbv[demo]
    ~/.local/bin/xcbv runserver

Resources
=========

- `**Documentation** graciously hosted
  <http://xcbv.readthedocs.io>`_ by `RTFD
  <http://rtfd.org>`_
- `Mailing list graciously hosted
  <http://groups.google.com/group/yourlabs>`_ by `Google
  <http://groups.google.com>`_
- For **Security** issues, please contact yourlabs-security@googlegroups.com
- `Git graciously hosted
  <https://github.com/yourlabs/xcbv/>`_ by `GitHub
  <http://github.com>`_,
- `Package graciously hosted
  <http://pypi.python.org/pypi/xcbv/>`_ by `PyPi
  <http://pypi.python.org/pypi>`_,
- `Continuous integration graciously hosted
  <http://circleci.com/gh/yourlabs/xcbv>`_ by `CircleCI
  <http://circleci.com>`_
- `**Online paid support** provided via HackHands
  <https://hackhands.com/jpic/>`_,
