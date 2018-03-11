from xcbv import shortcuts as xcbv

from .models import Person, Pet, Toy


class PetRouter(xcbv.Router):
    model = Pet
    routes = [
        xcbv.ListView,
        xcbv.Router(
            xcbv.ListView,
            model=Toy,
        )
    ]


router = xcbv.Router(
    app_name='full',
    # namespace = full
    routes=[
        xcbv.Router(
            xcbv.ListView,
            xcbv.CreateView,
            xcbv.UpdateView,
            xcbv.DeleteView,
            xcbv.DetailView,
            PetRouter,
            model=Person,
            # app_name = full
            # namespace = person
        )
    ]
)
