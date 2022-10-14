from pathlib import Path
#
# from django.views.generic import detail
# from .pages import IndexPage
from ..transform_toolbox.academy_csv import AcademyCSV
from ..transform_toolbox.talent_csv import TalentCSV
from ..transform_toolbox.talent_json import TalentJSON
from ..transform_toolbox.talent_txt import TalentTXT
import pandas as pd
# from .factory import factory
# from .models import *
from ..load_data import LoadData
from ..extract_files import ExtractFiles
#
#
# def index(request):
#     # factory.standard_factory()  # fake data - test front end
#
    # pickle_jar_path = Path(__file__).parent.resolve() / "pickle_jar"
    # load = LoadData()
#
    # # import pickles (temporary)
    # raw_academy_csv_df = pd.read_pickle(pickle_jar_path / "academy_csv_v2.pkl")
    # raw_talent_csv_df = pd.read_pickle(pickle_jar_path / "talent_csv_v2.pkl")
    # raw_talent_json_df = pd.read_pickle(pickle_jar_path / "talent_json.pkl")
    # raw_talent_txt_df = pd.read_pickle(pickle_jar_path / "talent_txt_v2.pkl")
#
#     # instantiate transform classes
#     academy_csv_transform = AcademyCSV(raw_academy_csv_df)
#     talent_csv_transform = TalentCSV()
#     talent_json_transform = TalentJSON(raw_talent_json_df)
#     talent_txt_transform = TalentTXT()
#
    # # get
    # trainer_df, course_df, academy_performance_df = academy_csv_transform.transform_academy_csv()
    # student_information_df, invitation_df = talent_csv_transform.transform_talent_csv(raw_talent_csv_df)
    # (
    #     trainee_performance_df,
    #     weakness_junction_df,
    #     strength_junction_df,
    #     tech_self_score_junction_df
    # ) = talent_json_transform.transform_talent_json()
    # test_score_df = talent_txt_transform.transform_talent_txt(raw_talent_txt_df)
#
#     load.trainer(trainer_df)
#     load.strength(strength_junction_df)
#     load.weakness(weakness_junction_df)


def run():
    extract_files = ExtractFiles("data32-final-project-files")

    # academy_csv_df, academy_csv_filenames_df = extract_files.get_files_as_df([], 'Academy', '.csv', filename_in_df=True)
    # talent_csv_df, talent_csv_filenames_df = extract_files.get_files_as_df([], 'Talent', '.csv', filename_in_df=True)
    # talent_txt_df, talent_txt_filenames_df = extract_files.get_files_as_df([], 'Talent', '.txt', filename_in_df=True)
    # talent_json_df, talent_json_filenames_df = extract_files.get_files_as_df([], 'Talent', '.json', filename_in_df=False)

    # import pickles (debug)
    pickle_jar_path = Path(__file__).parent.parent.resolve() / "pickle_jar"
    raw_academy_csv_df = pd.read_pickle(pickle_jar_path / "academy_csv_v2.pkl")
    raw_talent_csv_df = pd.read_pickle(pickle_jar_path / "talent_csv_v2.pkl")
    raw_talent_json_df = pd.read_pickle(pickle_jar_path / "talent_json.pkl")
    raw_talent_txt_df = pd.read_pickle(pickle_jar_path / "talent_txt_v2.pkl")

    # instantiate transform classes
    academy_csv_transform = AcademyCSV(raw_academy_csv_df)
    talent_csv_transform = TalentCSV()
    talent_json_transform = TalentJSON(raw_talent_json_df)
    talent_txt_transform = TalentTXT()

    trainer_df, course_df, academy_performance_df = academy_csv_transform.transform_academy_csv()
    student_information_df, invitation_df = talent_csv_transform.transform_talent_csv(raw_talent_csv_df)
    (trainee_performance_df, weakness_junction_df, strength_junction_df,
     tech_self_score_junction_df) = talent_json_transform.transform_talent_json()
    test_score_df = talent_txt_transform.transform_talent_txt(raw_talent_txt_df)

    load = LoadData()
    load.trainer(trainer_df)
    load.strength(strength_junction_df)
    load.weakness(weakness_junction_df)
    load.tech_self_score(tech_self_score_junction_df)
    load.invitation(invitation_df)
    load.test_score(test_score_df)
    load.course(course_df)
    load.academy_performance(academy_performance_df)
    load.trainee_performance(trainee_performance_df)
    load.student_information(student_information_df)
