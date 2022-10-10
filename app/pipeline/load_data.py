import pandas as pd
from .models import (
    StudentInformation,
    TraineePerformance,
    AcademyPerformance,
    Course,
    Trainer,
    TechScore,
    Strength,
    Weakness,
    Invitation,
    TestScore
)


class LoadData:
    def __init__(self):
        pass

    def student_information(self, df: pd.DataFrame) -> None:
        pass

    def trainee_performance(self, df: pd.DataFrame, student_info_df: pd.DataFrame) -> None:
        pass

    def academy_performance(self, df: pd.Series) -> None:
        academy_performance_obj = AcademyPerformance(
            week=df["week"],
            analytic=df["Analytic"],
            independent=df["Independent"],
            determined=df["Determined"],
            professional=df["Professional"],
            studious=df["Studious"],
            imaginative=df["Imaginative"]
        )
        academy_performance_obj.save()

    def course(self, df: pd.DataFrame, trainer_df: pd.DataFrame) -> None:
        pass

    def trainer(self, df: pd.DataFrame) -> None:
        pass

    def test_score(self, df: pd.DataFrame) -> None:
        pass

    def strength(self, df: pd.DataFrame) -> None:
        pass

    def weakness(self, df: pd.DataFrame) -> None:
        pass

    def invitation(self, df: pd.DataFrame) -> None:
        pass

    def tech_score(self, df: pd.DataFrame) -> None:
        pass
