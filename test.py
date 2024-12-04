from dataclasses import dataclass

from openapidocs.v3 import Info

from blacksheep import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler

parent = Application(show_error_details=True)
parent.mount_registry.auto_events = True
parent.mount_registry.handle_docs = True


docs = OpenAPIHandler(info=Info(title='Parent API', version='0.0.1'))
docs.bind_app(parent)


@dataclass
class CreateCatInput:
    name: str
    email: str
    foo: int


@dataclass
class CreateDogInput:
    name: str
    email: str
    example: int


@dataclass
class CreateParrotInput:
    name: str
    email: str


@parent.router.get('/')
def a_home():
    """Parent root."""
    return 'Hello, from the parent app - for information, navigate to /docs'


@parent.router.get('/cats')
def get_cats_conflicting():
    """Conflict!"""
    return 'CONFLICT'


child_1 = Application()


@child_1.router.get('/')
def get_cats():
    """Gets a list of cats."""
    return 'Gets a list of cats.'


@child_1.router.post('/')
def create_cat(data: CreateCatInput):
    """Creates a new cat."""
    return 'Creates a new cat.'


@child_1.router.delete('/{cat_id}')
def delete_cat(cat_id: str):
    """Deletes a cat by id."""
    return 'Deletes a cat by id.'


child_2 = Application()


@child_2.router.get('/')
def get_dogs():
    """Gets a list of dogs."""
    return 'Gets a list of dogs.'


@child_2.router.post('/')
def create_dog(data: CreateDogInput):
    """Creates a new dog."""
    return 'Creates a new dog.'


@child_2.router.delete('/{dog_id}')
def delete_dog(dog_id: str):
    """Deletes a dog by id."""
    return 'Deletes a dog by id.'


child_3 = Application()


@child_3.router.get('/')
def get_parrots():
    """Gets a list of parrots."""
    return 'Gets a list of parrots'


@child_3.router.post('/')
def create_parrot(data: CreateParrotInput):
    """Creates a new parrot."""
    return 'Creates a new parrot'


@child_3.router.delete('/{parrot_id}')
def delete_parrot(parrot_id: str):
    """Deletes a parrot by id."""
    return 'Deletes a parrot by id.'


parent.mount('/cats', child_1)
parent.mount('/dogs', child_2)
parent.mount('/parrots', child_3)
