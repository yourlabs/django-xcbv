from xcbv import shortcuts as xcbv

from .models import Person, Pet, Toy


PersonRouter = xcbv.Router(
    xcbv.DetailView.factory(
        xcbv.ListView.factory(
            xcbv.DetailView.factory(
                xcbv.ListView.factory(
                    xcbv.DetailView.factory(pk_url_kwarg='toy'),
                    model=Toy
                ),
                pk_url_kwarg='pet',
            ),
            model=Pet,
        ),
    ),
    model=Person,
)
