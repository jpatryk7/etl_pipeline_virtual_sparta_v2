from pathlib import Path

from django.views.generic import detail
from .pages import IndexPage
from .models import StudentInformation


def index(request):
    # factory.standard_factory()  # fake data - test front end
    return IndexPage()


class TestModelDetailView(detail.DetailView):
    model = StudentInformation
    template_name = 'test-detail.html'
