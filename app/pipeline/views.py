from django.views.generic import detail
from .pages import IndexPage
from .factory import factory

from .models import *


def index(request):
    factory.standard_factory()
    return IndexPage()


class TestModelDetailView(detail.DetailView):
    model = StudentInformation
    template_name = 'test-detail.html'
