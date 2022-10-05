from iommi import Table, Page
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
        columns__student_information_id__cell__url=lambda row, **_: row.get_absolute_url(),
    )
    academy_performance_table = Table(
        auto__model=AcademyPerformance,
        page_size=20,
        columns__student_information_id__cell__url=lambda row, **_: row.get_absolute_url(),
    )
    course_table = Table(
        auto__model=Course,
        page_size=10,
        columns__course_name__filter__include=True,
        columns__course_name__cell__url=lambda row, **_: row.get_absolute_url(),
    )
    trainer_table = Table(
        auto__model=Trainer,
        page_size=10,
    )
