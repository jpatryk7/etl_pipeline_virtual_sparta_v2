from django.views.generic import detail
from .pages import IndexPage
import pandas as pd
from .factory import factory
from .transform_toolbox_old.split_academy_csv_df import SplitAcademyCSVFrame
from .models import *
from .load_data import LoadData
from .extract_files import ExtractFiles


def index(request):
    factory.standard_factory()
    # ex = ExtractFiles("data32-final-project-files")
    # s = SplitAcademyCSVFrame(ex.get_files_as_df([], 'Academy', '.csv')[0])
    # df = s.get_academy_performance_df()
    # ld = LoadData()
    # for _, row in df.iterrows():
    #     ld.academy_performance(row)
    return IndexPage()


class TestModelDetailView(detail.DetailView):
    model = StudentInformation
    template_name = 'test-detail.html'
