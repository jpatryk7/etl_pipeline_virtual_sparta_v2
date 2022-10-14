import datetime
from typing import Type

import numpy as np
import pandas as pd
from .models import (
    models,
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
        self.trainer_df = pd.DataFrame([])
        self.course_df = pd.DataFrame([])
        self.academy_performance_df = pd.DataFrame([])
        self.invitation_df = pd.DataFrame([])
        self.trainee_performance_df = pd.DataFrame([])
        self.weakness_junction_df = pd.DataFrame([])
        self.strength_junction_df = pd.DataFrame([])
        self.tech_self_score_junction_df = pd.DataFrame([])
        self.test_score_df = pd.DataFrame([])

    @staticmethod
    def _df_to_sql(df: pd.DataFrame, model: Type[models.Model]) -> None:
        # credit to: pandichef @ https://github.com/chrisdev/django-pandas/issues/125
        dct = df.replace({np.nan: None}).to_dict("records")  # replace NaN with None since Django doesn't understand NaN
        bulk_list = []
        for x in dct:
            bulk_list.append(model(**x))
        model.objects.bulk_create(bulk_list)

    def student_information(self, student_information_df: pd.DataFrame) -> None:
        for _, row in student_information_df.iterrows():
            test_score_mask = self.test_score_df["student_name"] == row["student_name"]
            test_score = pd.DataFrame(self.test_score_df[test_score_mask])
            # test_score = self.test_score_df.loc[
            #     (self.test_score_df["student_name"] == row["student_name"])
            #     and (self.test_score_df["date"] == row["date"])
            # ]
            test_score_obj_instance = TestScore.objects.filter(
                psychometrics=test_score["psychometrics"],
                presentation=test_score["presentation"])

            #
            invitation_mask = self.invitation_df["student_name"] == row["student_name"]
            invitation = pd.DataFrame(self.invitation_df[invitation_mask])
            # invitation = self.invitation_df.loc[
            #     (self.invitation_df["student_name"] == row["student_name"])
            #     and (self.invitation_df["date"] == row["date"])
            # ]
            invitation_obj_instance = Invitation.objects.filter(
                invited_date=invitation["invited_date"],
                invited_by=invitation["invited_by"])

            #
            academy_performance_mask = self.academy_performance_df["student_name"] == row["student_name"]
            academy_performance = pd.DataFrame(self.academy_performance_df[academy_performance_mask])
            # academy_performance = self.academy_performance_df.loc[
            #     (self.academy_performance_df["student_name"] == row["student_name"])
            #     and (self.academy_performance_df["date"] == row["date"])
            # ]
            academy_performance_obj_instance = AcademyPerformance.objects.filter(
                week=academy_performance["week"],
                analytic=academy_performance["analytic"],
                independent=academy_performance["independent"],
                determined=academy_performance["determined"],
                professional=academy_performance["professional"],
                studious=academy_performance["studious"],
                imaginative=academy_performance["imaginative"]
            )

            #
            trainee_performance_mask = self.trainee_performance_df["student_name"] == row["student_name"]
            trainee_performance = pd.DataFrame(self.trainee_performance_df[trainee_performance_mask])
            # trainee_performance = self.trainee_performance_df.loc[
            #     (self.trainee_performance_df["student_name"] == row["student_name"])
            #     and (self.trainee_performance_df["date"] == row["date"])
            # ]
            trainee_performance_obj_instance = TraineePerformance.objects.filter(
                self_development=trainee_performance["self_development"],
                geo_flex=trainee_performance["geo_flex"],
                financial_support=trainee_performance["financial_support"],
                course_interest=trainee_performance["course_interest"]
            )

            obj = StudentInformation(
                student_name=row["student_name"],
                gender=row["gender"],
                dob=row["dob"],
                email=row["email"],
                city=row["city"],
                address=row["address"],
                postcode=row["postcode"],
                university=row["university"],
                degree=row["degree"],
                test_score_id=test_score_obj_instance,
                invitation_id=invitation_obj_instance,
                academy_performance_id=academy_performance_obj_instance,
                trainee_performance_id=trainee_performance_obj_instance
            )
            obj.save()

    def trainee_performance(self, trainee_performance_df: pd.DataFrame) -> None:
        """
        columns: {"student_name", "date", "self_development", "geo_flex", "financial_support", "result",
        "course_interest"} -> {"self_development", "geo_flex", "financial_support",
        "course_interest"} (no duplicates)
        """
        self.trainee_performance_df = trainee_performance_df
        self._df_to_sql(trainee_performance_df[["self_development", "geo_flex", "financial_support", "course_interest"]], TraineePerformance)
        # for _, row in tech_self_score_junction_df.iterrows():
        #     trainee_perf_row = trainee_performance_df.loc[
        #         trainee_performance_df["student_name"] == row["student_name"]
        #         and trainee_performance_df["date"] == row["date"]]
        #     trainee_performance_obj = TraineePerformance.objects.filter(
        #         self_development=trainee_perf_row["self_development"],
        #         geo_flex=trainee_perf_row["geo_flex"]
        #     )
        # for _, row in strength_junction_df.iterrows():
        #     trainee_perf_row = trainee_performance_df.loc[
        #         trainee_performance_df["student_name"] == row["student_name"]
        #         and trainee_performance_df["date"] == row["date"]]
        #     trainee_performance_obj = TraineePerformance.objects.filter(
        #         self_development=trainee_perf_row["self_development"],
        #         geo_flex=trainee_perf_row["geo_flex"]
        #     )
        # for _, row in weakness_junction_df.iterrows():
        #     trainee_perf_row = trainee_performance_df.loc[
        #         trainee_performance_df["student_name"] == row["student_name"]
        #         and trainee_performance_df["date"] == row["date"]]
        #     trainee_performance_obj = TraineePerformance.objects.filter(
        #         self_development=trainee_perf_row["self_development"],
        #         geo_flex=trainee_perf_row["geo_flex"],
        #
        #     )

    def academy_performance(self, academy_performance_df: pd.DataFrame) -> None:
        """
        columns: {"student_name", "date", "course_name", "week", "analytic", "independent", "determined",
        "professional", "studious", "imaginative"} -> {"course_id", "week", "analytic", "independent", "determined",
        "professional", "studious", "imaginative"} (no duplicates)
        """
        self.academy_performance_df = academy_performance_df
        for _, row in academy_performance_df.iterrows():
            course_instance = Course.objects.filter(course_name=row["course_name"])[0]
            obj = AcademyPerformance(
                course_id=course_instance,
                week=int(row["week"][1:]),
                analytic=row["analytic"],
                independent=row["independent"],
                determined=row["determined"],
                professional=row["professional"],
                studious=row["studious"],
                imaginative=row["imaginative"]
            )
            obj.save()

    def course(self, course_df: pd.DataFrame) -> None:
        """
        columns: {"course_name", "trainer_name", "date"} -> {"course_name", "trainer_id"}
        """
        self.course_df = course_df
        for _, row in course_df.iterrows():
            trainer_instance = Trainer.objects.filter(trainer_name=row["trainer_name"])[0]
            obj = Course(
                course_name=row["course_name"],
                trainer_id=trainer_instance
            )
            obj.save()

    def trainer(self, trainer_df: pd.DataFrame) -> None:
        """
        columns: {"trainer_name"}
        """
        self.trainer_df = trainer_df
        self._df_to_sql(trainer_df, Trainer)

    def test_score(self, test_score_df: pd.DataFrame) -> None:
        """
        columns: {"student_name", "date", "psychometrics", "presentation"}
        -> {"psychometrics", "presentation"} (no duplicates)
        """
        self.test_score_df = test_score_df
        self._df_to_sql(test_score_df[["psychometrics", "presentation"]].drop_duplicates().dropna(), TestScore)

    def strength(self, strength_df: pd.DataFrame) -> None:
        """
        columns: {"student_name", "date", "strength"} -> {"strength"} (no duplicates)
        """
        self.strength_junction_df = strength_df
        self._df_to_sql(strength_df["strength"].to_frame().drop_duplicates().dropna(), Strength)

    def weakness(self, weakness_df: pd.DataFrame) -> None:
        """
        columns: {"student_name", "date", "weakness"} -> {"weakness"} (no duplicates)
        """
        self.weakness_junction_df = weakness_df
        self._df_to_sql(weakness_df["weakness"].to_frame().drop_duplicates().dropna(), Weakness)

    def invitation(self, invitation_df: pd.DataFrame) -> None:
        """
        columns: {"student_name", "date", "invited_date", "invited_by"}
        -> {"invited_date", "invited_by"} (no duplicates)
        """
        invitation_df["invited_date"] = invitation_df["invited_date"].apply(lambda ls: datetime.date(ls[2], ls[1], ls[0]) if ls else None)
        self.invitation_df = invitation_df
        self._df_to_sql(invitation_df[["invited_date", "invited_by"]].drop_duplicates().dropna(), Invitation)

    def tech_self_score(self, tech_self_score_df: pd.DataFrame) -> None:
        """
        columns: {"student_name", "date", "tech_self_score", "value"} -> {"tech_self_score", "value"} (no duplicates)
        """
        self.tech_self_score_junction_df = tech_self_score_df
        self._df_to_sql(tech_self_score_df[["tech_self_score", "value"]].drop_duplicates().dropna(), TechScore)
