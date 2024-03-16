class Man:
    name: str
    age: int


a = Man


def mm(**kwargs):
    print(kwargs)
    for key, values in kwargs.items():
        if not hasattr(a, key):
            raise


mm(name="Denis", age=28)
