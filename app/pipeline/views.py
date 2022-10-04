from django.shortcuts import render
from django.views.generic import list, detail
from iommi import Table

############################
#  TEST VIEW REMOVE LATER  #
############################

from .models import TestModel


def test_model_list_view(request):
    return Table(
        auto__model=TestModel,
        page_size=20,
        columns__field_one__filter__include=True,
        columns__field_one__cell__url=TestModel.id
    )


class TestModelDetailView(detail.DetailView):
    model = TestModel
    template_name = 'test-detail.html'
