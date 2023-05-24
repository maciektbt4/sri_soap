from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from spyne.error import ResourceNotFoundError, ResourceAlreadyExistsError
from spyne.server.django import DjangoApplication
from spyne.model.primitive import Unicode, Integer
from spyne.model.complex import Iterable
from spyne.model.complex import Array
from spyne.service import Service
from spyne.protocol.soap import Soap11
from spyne.application import Application
from spyne.decorator import rpc
from spyne.util.django import DjangoComplexModel, DjangoService
from .models import Person
from .serializers import PersonSerializer


class PersonContainer(DjangoComplexModel):
    class Attributes(DjangoComplexModel.Attributes):
        django_model = Person
        #django_exclude = ['excluded_field']

class HelloWorldService(Service):
    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(ctx, name, times):
        for i in range(times):
            yield 'Hello, %s' % name


class PersonService(Service):
    @rpc(Integer, _returns=PersonContainer)
    def get_person(ctx, pk):
        try:
            return Person.objects.get(pk=pk)
        except Person.DoesNotExist:
            raise ResourceNotFoundError('PersonContainer')
    
    @rpc(_returns=Array(PersonContainer))
    def get_all_persons(ctx):
        try:
            persons = Person.objects.all()            
            return persons
            
        except Person.DoesNotExist:
            raise ResourceNotFoundError('PersonContainer')

    @rpc(PersonContainer, _returns=PersonContainer)
    def create_person(ctx, container):
        try:
            return Person.objects.create(**container.as_dict())
        except IntegrityError:
            raise ResourceAlreadyExistsError('PersonContainer')
    
    @rpc(Integer,_returns=Unicode)
    def delete_person(ctx, pk):
        try:
            person_to_delete = Person.objects.filter(pk=pk)
            person_to_delete.delete()
            
            return f"Person id = {pk} has been deleted"
        except IntegrityError:
            raise ResourceAlreadyExistsError('PersonContainer')

    @rpc(Integer,PersonContainer, _returns=PersonContainer)
    def update_person(ctx, pk,  container):
        try:
            person = Person.objects.get(pk = pk)  
            data = container.as_dict()
            serializer=PersonSerializer(person, data=data)
            serializer.is_valid()
            serializer.save()
            return person
        except IntegrityError:
            raise ResourceAlreadyExistsError('PersonContainer')
        
class ExceptionHandlingService(DjangoService):

    """Service for testing exception handling."""

    @rpc(_returns=PersonContainer)
    def raise_does_not_exist(ctx):
        return Person.objects.get(pk=-1)


app = Application([HelloWorldService, PersonService,
                   ExceptionHandlingService],
    'spyne.examples.django',
    in_protocol=Soap11(),
    out_protocol=Soap11(),
)


hello_world_service = csrf_exempt(DjangoApplication(app))
