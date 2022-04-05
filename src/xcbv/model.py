import copy
import inspect

from django.db import models


def model_factory(cls, app_label=None, model_name=None,
                  verbose_name=None, verbose_name_plural=None):
    model = type(
        cls.__name__.lower(),
        (cls, models.Model),
        dict(
            _meta=type('Meta', (object,), dict(managed=False)),
        )
    )
    return model
