from iommi import Table, Page, Column
from .models import StudentInformation, TraineePerformance, AcademyPerformance, Course, Trainer


class IndexPage(Page):
    student_information_table = Table(
        auto__model=StudentInformation,
        page_size=20,
        columns__name__filter__include=True,
        columns__name__cell__url=lambda row, **_: row.get_absolute_url(),
    )
    trainee_performance_table = Table(
        auto__model=TraineePerformance,
        page_size=20,
        columns__student_name=Column(
            cell__value=lambda row, **_: row.get_student_name(),
            cell__url=lambda row, **_: row.get_student_absolute_url(),
        ),
    )
    academy_performance_table = Table(
        auto__model=AcademyPerformance,
        page_size=20,
        columns__student_name=Column(
            cell__value=lambda row, **_: row.get_student_name(),
            cell__url=lambda row, **_: row.get_student_absolute_url(),
        ),
    )
    course_table = Table(
        auto__model=Course,
        page_size=10,
        columns__course_name__filter__include=True,
        columns__trainer_id__include=False,
        columns__trainer_name=Column(
            cell__value=lambda row, **_: row.get_trainer_name()
        ),
        # columns__students=Column(
        #     cell__value=lambda row, **_: row.get_all_student_names(),
        #     cell__url=lambda row, **_: row.get_all_student_absolute_urls(),
        # ),
    )
    trainer_table = Table(
        auto__model=Trainer,
        page_size=10,
    )
