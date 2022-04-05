"""xCBV generic views and bases."""
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from .route import Route


class ViewMixin(Route):
    """Base View mixin for xcbv."""


class View(ViewMixin, generic.View):
    """Base view for CRUDLFA+."""


class TemplateViewMixin(ViewMixin):
    """
    Override for get_template_names to append default_template_name.

    This allows to configure "last resort" templates for each class, and thus
    to provide a working CRUD out of the box.
    """

    def get_title_html(self):
        """Return text for HTML title tag."""
        return self.title

    def get_title_heading(self):
        """Return text for page heading."""
        return self.title

    def get_template_names(self):
        """Give a chance to default_template_name."""
        template_names = super().get_template_names()
        default_template_name = getattr(self, 'default_template_name', None)
        if default_template_name:
            template_names.append(default_template_name)
        return template_names



class TemplateView(TemplateViewMixin, generic.TemplateView):
    """Template view with default_template_name support."""


class ModelViewMixin(ViewMixin):
    """Mixin for views using a Model class but no instance."""

    menus = ['model']

    @property
    def title(self):
        return '{} {}'.format(
            _(self.slug),
            self.model._meta.verbose_name_plural,
        ).capitalize()

    @property
    def fields(self):
        """Return router fields."""
        return self.router.fields_filter(lambda f: True)

    @property
    def exclude(self):
        """Return router.exclude or None, field names if ``__all__``.."""
        return getattr(self.router, 'ecxlude', None)

    def get_queryset(self):
        """Return router.get_queryset() by default, otherwise super()."""
        router = getattr(self, 'router', None)
        if getattr(router, 'get_queryset', None):
            return router.get_queryset(self)
        return super().get_queryset()


class ModelView(ModelViewMixin, View):
    """Base view for a model."""


class ObjectMixin(object):
    """
    Make self.object call and cache self.get_object() automatically.

    WHAT A RELIEF

    However, if it has a router with the get_object() method, use it.
    """

    def get_object(self):
        """Return router.get_object() by default, otherwise super()."""
        router = getattr(self, 'router', None)
        if router and getattr(router, 'get_object', None):
            return router.get_object(self)

        if getattr(self, 'kwargs', False) is False:
            # This happens when the view has not been instanciated with an
            # object, neither from a URL which would allow getting the object
            # in the super() call below.
            raise Exception('Must instanciate the view with an object')
        return super().get_object()

    def object_get(self):
        """Return the object, uses get_object() if necessary."""
        cached = getattr(self, '_object', None)
        if not cached:
            self._object = self.get_object()
        return self._object

    def object_set(self, value):
        """Set self.object attribute."""
        self._object = value

    object = property(object_get, object_set)


class ObjectViewMixin(ObjectMixin, ModelViewMixin):
    """Mixin for views using a Model instance."""

    menus = ['object']

    def get_url_args(self):
        """Return ``[self.object]``."""
        return [self.object]

    def get_slug_field(self):
        """Replace Django's get_slug_field with get_url_field."""
        return self.get_url_field()

    @property
    def slug_url_kwarg(self):
        """Replace Django's slug_url_kwarg with get_url_field."""
        return self.get_url_field()

    @classmethod
    def get_url_field(cls):
        """
        Return the model field name to use in the url.

        By default, try router's url_field, otherwise try ``slug``,
        fallback on ``pk``.
        """
        url_field = getattr(cls, 'url_field', None)
        if url_field is None:
            router = getattr(cls, 'router', None)
            return router.url_field

        return url_field or 'pk'

    @classmethod
    def to_url_args(cls, *args):
        """Return first arg's url_field attribute."""
        url_field = cls.get_url_field()
        return [getattr(args[0], url_field)]

    @classmethod
    def get_path(cls):
        """Identify the object by slug or pk in the pattern."""
        if 'slug' in cls.model._meta.fields:
            return '{}/<slug>/'.format(cls.name)

        return '{}/<pk>/'.format(cls.name)

    @property
    def title(self):
        return '{} {} "{}"'.format(
            _(self.slug),
            self.model._meta.verbose_name,
            self.object
        ).capitalize()


class FormViewMixin(ViewMixin):
    """Mixin for views which have a Form."""
    success_url_next = True

    def get_success_url(self):
        url = super().get_success_url()
        if self.success_url_next and '_next' in self.request.POST:
            url = self.request.POST['_next']
        return url


class FormView(FormViewMixin, generic.FormView):
    """Base FormView class."""

    style = 'warning'
    default_template_name = 'form.html'


class ModelFormViewMixin(ModelViewMixin, FormViewMixin):
    """ModelForm ViewMixin using readable"""

    @property
    def fields(self):
        """Return router.fields_editable."""
        return self.router.fields_filter(lambda f: f.editable)

    def form_invalid(self, form):
        messages.error(
            self.request,
            _(
                '{} {} error'.format(
                    self.slug,
                    self.model._meta.verbose_name
                ).capitalize()
            )
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(
            self.request,
            _(
                '%s %s: {}' % (self.slug, self.model._meta.verbose_name)
            ).format(form.instance).capitalize()
        )
        return super().form_valid(form)


class ObjectFormViewMixin(ObjectViewMixin, ModelFormViewMixin):
    """Custom form view mixin on an object."""


class ObjectFormView(ObjectFormViewMixin, generic.FormView):
    """Custom form view on an object."""


class CreateView(ModelFormViewMixin, generic.CreateView):
    """View to create a model object."""

    style = 'success'
    fa_icon = 'plus'
    material_icon = 'add'
    default_template_name = 'create.html'
    ajax = '_modal'


class DeleteView(ObjectFormViewMixin, generic.DeleteView):
    """View to delete a model object."""

    default_template_name = 'delete.html'
    style = 'danger'
    fa_icon = 'trash'
    material_icon = 'delete'
    color = 'red'
    ajax = '_modal'
    success_url_next = True

    def get_success_url(self):
        messages.success(
            self.request,
            _(
                '%s %s: {}' % (self.slug, self.model._meta.verbose_name)
            ).format(self.object).capitalize()
        )
        return self.router['list'].reverse()


class DetailView(ObjectViewMixin, generic.DetailView):
    """Templated model object detail view which takes a field option."""

    fa_icon = 'search-plus'
    material_icon = 'search'
    default_template_name = 'detail.html'
    color = 'green'

    @property
    def title(self):
        return str(self.object)

    def get_context_data(self, *a, **k):
        c = super(DetailView, self).get_context_data(*a, **k)
        c['fields'] = [
            {
                'field': self.model._meta.get_field(field),
                'value': getattr(self.object, field)
            }
            for field in self.fields
        ]
        return c

    @classmethod
    def get_regex(cls):
        """Identify the object by slug or pk in the pattern."""
        try:
            cls.model._meta.get_field(self.slug_url_kwarg)
        except:
            arg = cls.pk_url_kwarg
        else:
            arg = cls.slug_url_kwarg

        return '<{}>'.format(arg)


class ListView(ModelViewMixin, generic.ListView):
    """Model list view."""

    default_template_name = 'list.html'
    url_pattern = '$'
    paginate_by = 10
    fa_icon = 'table'
    material_icon = 'list'
    menus = ['main']
    color = 'green'


class UpdateView(ObjectFormViewMixin, generic.UpdateView):
    """Model update view."""

    fa_icon = 'edit'
    material_icon = 'edit'
    default_template_name = 'update.html'
    ajax = '_modal'
    color = 'orange'
