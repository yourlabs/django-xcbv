from xcbv import xcbv

from .models import Person, Pet, Toy


class PetRouter(xcbv.Router):
    model = Pet
    children = [
        xcbv.ListView,
        xcbv.CreateView,
        xcbv.DetailView,
        xcbv.ListView,
        xcbv.DetailView,
        xcbv.Router.factory(
            xcbv.ListView,
            xcbv.CreateView,
            xcbv.DetailView,
            xcbv.ListView,
            xcbv.DetailView,
            model=Toy,
        )
    ]


router = xcbv.Router(
    app_name='full',
    # namespace = full
    children=[
        xcbv.Router(
            xcbv.ListView,
            xcbv.CreateView,
            xcbv.DetailView,
            xcbv.ListView,
            xcbv.DetailView,
            PetRouter,
            model=Person,
            # app_name = full
            # namespace = person
        )
    ]
)
