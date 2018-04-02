from xcbv import shortcuts as xcbv

from .models import Person, Pet, Toy


class PetListView(xcbv.ListView):
    model = Pet
    routes = [
        xcbv.DetailView.factory(
            xcbv.ListView.factory(model=Toy),
            pk_url_kwarg='pet_pk',
        ),
    ]


PersonIndex = xcbv.ModelView.factory(
    xcbv.ListView,
    xcbv.CreateView,
    xcbv.UpdateView,
    xcbv.DeleteView,
    xcbv.DetailView.factory(PetListView),
    model=Person,
    app_name='full',
)
