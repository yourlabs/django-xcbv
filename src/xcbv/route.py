

class RouteMetaclass(type):
    parent = None

    def factory(cls, **attributes):
        name = cls.__name__
        return type(name, (cls,), attributes)

    def __getattr__(cls, attr):
        if attr == 'namespace' and cls.parent:
            return cls.parent.namespace
        if attr == 'app_name' and cls.parent:
            return cls.parent.app_name
        return object.__getattr__(cls, attr)


class Route(metaclass=RouteMetaclass):
    pass
