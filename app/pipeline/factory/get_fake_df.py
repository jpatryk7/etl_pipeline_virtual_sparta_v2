from typing import Optional, Union
import pandas as pd
from faker import Faker
import random


class GetFakeDf:  # pragma: no cover
    """
    Example use:
        get_fake_df = GetFakeDf()
        _trainer_df, _course_df, _academy_performance_df = get_fake_df.fake_transform_academy_csv()
        _student_information_df, _invitation_df = get_fake_df.fake_transform_talent_csv()
        _trainee_performance_df, _weakness_junction_df, _strength_junction_df, _tech_self_score_junction_df = get_fake_df.fake_transform_talent_json()
        _test_score_df = get_fake_df.fake_transform_talent_txt()
    """
    def __init__(self, *, no_of_students: int = 200) -> None:
        self.no_of_students = no_of_students
        self.faker = Faker('en_US')
        self.faker.seed_instance(0)
        self.dt = pd.DataFrame({
            'float': [1.0],
            'int': [1],
            'object': ['foo'],
            'bool': [True]
        })
        self.student_date_df = self._get_student_date_df()
        self.course_df = pd.DataFrame([])

    @staticmethod
    def __df_builder(
            data: dict,
            dtypes: dict,
            no_of_entries: int,
            *, join_df: Optional[Union[pd.DataFrame, pd.Series, list[pd.DataFrame], list[pd.Series]]] = None) -> pd.DataFrame:
        """
        data = {key1: generator1, key2: generator2, ...}
        dtypes = {key1: dtype1, key2: dtype2, ...}
        e.g.
        data = {
            "student_name": lambda: self.faker.name(),
            "date": lambda: [
                random.randint(1, 29),
                random.randint(1, 13),
                random.randint(2015, 2021)
            ]
        }
        dtypes = {
            "student_name": self.dt['object'].dtype,
            "date": self.dt['object'].dtype
        }
        """
        data_dict = {key: [generator() for _ in range(no_of_entries)] for key, generator in data.items()}
        df = pd.DataFrame(data_dict)
        if join_df is not None:
            df = pd.concat([df, *join_df] if type(join_df) == list else [df, join_df], axis=1)
        return df.astype(dtypes)

    @staticmethod
    def __df_alter_len(df: Union[pd.DataFrame, pd.Series], *, new_df_len: Optional[int] = None, multiply: Optional[int] = None) -> Union[pd.DataFrame, pd.Series]:
        """
        Select at random new_df_len number of rows from df
        """
        if multiply:
            return pd.concat([df for _ in range(multiply)]).reset_index()
        elif new_df_len:
            old_index_list = df.index.tolist()
            return df.iloc[[random.choice(old_index_list) for _ in range(new_df_len)]].reset_index()

    def _get_student_date_df(self) -> pd.DataFrame:
        """
        base_df {"student_name", "date"}
        """
        data = {
            "student_name": lambda: self.faker.name(),
            "date": lambda: [random.randint(1, 28), random.randint(1, 12), random.randint(2015, 2021)]
        }
        dtypes = {
            "student_name": self.dt['object'].dtype,
            "date": self.dt['object'].dtype
        }
        return self.__df_builder(data, dtypes, self.no_of_students)

    def _get_trainer_df(self, no_of_entries: int) -> pd.DataFrame:
        """
        columns: {"trainer_name"}
        """
        data = {"trainer_name": lambda: self.faker.name()}
        dtypes = {"trainer_name": self.dt['object'].dtype}
        return self.__df_builder(data, dtypes, no_of_entries)

    def _get_course_df(self, trainer_df: pd.DataFrame, no_of_entries: Optional[int] = None) -> pd.DataFrame:
        """
        columns: {"course_name", "trainer_name", "date"}
        """
        if not no_of_entries:
            no_of_entries = len(trainer_df.index)

        data = {
            "course_name": lambda: self.faker.word(),
            "date": lambda: [random.randint(1, 29), random.randint(1, 13), random.randint(2015, 2021)]
        }
        dtypes = {
            "course_name": self.dt['object'].dtype,
            "date": self.dt['object'].dtype
        }
        return self.__df_builder(data, dtypes, no_of_entries, join_df=trainer_df)

    def _get_academy_performance_df(self, course_df: pd.DataFrame, *, frac: Optional[float] = .5) -> pd.DataFrame:
        """
        columns: {"student_name", "date", "course_name", "week", "analytic", "independent", "determined",
        "professional", "studious", "imaginative"}
        """
        if frac > 1:
            raise Exception(f"frac must be smaller or equal 1. Got {frac} instead.")

        no_of_entries = int(self.no_of_students * frac)

        col_names = ["week", "analytic", "independent", "determined", "professional", "studious", "imaginative"]
        data = {key: lambda: random.randint(0, 10) for key in col_names}
        dtypes = {key: self.dt['int'].dtype for key in col_names}
        student_date_df_subset = self.__df_alter_len(self.student_date_df, new_df_len=no_of_entries)
        course_df_superset = self.__df_alter_len(course_df, new_df_len=no_of_entries)
        return self.__df_builder(data, dtypes, no_of_entries, join_df=[course_df_superset, student_date_df_subset])

    def _get_student_information_df(self) -> pd.DataFrame:
        """
        columns: {"student_name", "date", "gender", "dob", "email", "city", "address", "postcode", "phone_number",
        "uni", "degree"}
        """
        data = {
            "gender": lambda: random.choice(['Male', 'Female', '']),
            "dob": lambda: [random.randint(1, 28), random.randint(1, 12), random.randint(1980, 2000)],
            "email": lambda: self.faker.ascii_free_email(),
            "city": lambda: self.faker.city(),
            "address": lambda: self.faker.street_address(),
            "postcode": lambda: random.choice(['AA9A', 'A9A', 'A9', 'A99', 'AA9', 'AA99']),
            "phone_number": lambda: self.faker.phone_number(),
            "uni": lambda: self.faker.company(),
            "degree": lambda: random.choice(['', '3rd', '2:2', '2:1', '1st'])
        }
        dtypes = {key: self.dt['object'].dtype for key in data.keys()}
        return self.__df_builder(data, dtypes, self.no_of_students, join_df=self.student_date_df)

    def _get_invitation_df(self) -> pd.DataFrame:
        """
        columns: {"student_name", "date", "invited_date", "invited_by"}
        """
        data = {
            "invited_date": lambda: [random.randint(1, 28), random.randint(1, 12), random.randint(2015, 2021)],
            "invited_by": lambda: self.faker.name(),
        }
        dtypes = {key: self.dt['object'].dtype for key in data.keys()}
        return self.__df_builder(data, dtypes, self.no_of_students, join_df=self.student_date_df)

    def _get_trainee_performance_df(self, course_df: pd.DataFrame, *, frac: Optional[float] = .75) -> pd.DataFrame:
        """
        columns: {"student_name", "date", "self_development", "geo_flex", "financial_support", "result",
        "course_interest"}
        """
        no_of_entries = int(self.no_of_students * frac)
        data = {
            "self_development": lambda: self.faker.pybool(),
            "geo_flex": lambda: self.faker.pybool(),
            "financial_support": lambda: self.faker.pybool(),
            "result": lambda: random.choice(["Pass", "Fail"]),
            "course_interest": lambda: random.choice(course_df["course_name"].tolist())
        }
        dtypes = {
            "self_development": self.dt['bool'].dtype,
            "geo_flex": self.dt['bool'].dtype,
            "financial_support": self.dt['bool'].dtype,
            "result": self.dt['object'].dtype,
            "course_interest": self.dt['object'].dtype
        }
        student_date_df_subset = self.__df_alter_len(self.student_date_df, new_df_len=no_of_entries)
        return self.__df_builder(data, dtypes, no_of_entries, join_df=student_date_df_subset)

    def _get_weakness_junction_df(self, trainee_performance_df: pd.DataFrame, *, relation_multiplicity: int = 5) -> pd.DataFrame:
        """
        columns: {"student_name", "date", "weakness"}
        """
        student_date_superset = self.__df_alter_len(trainee_performance_df[["student_name", "date"]],
                                                    multiply=relation_multiplicity)
        weakness_list = [self.faker.word() for _ in range(relation_multiplicity ** 2)]
        data = {
            "weakness": lambda: random.choice(weakness_list)
        }
        dtypes = {
            "weakness": self.dt['object'].dtype
        }
        return self.__df_builder(data, dtypes, len(student_date_superset.index), join_df=student_date_superset[["student_name", "date"]])

    def _get_strength_junction_df(self, trainee_performance_df: pd.DataFrame, *, relation_multiplicity: int = 5) -> pd.DataFrame:
        """
        columns: {"student_name", "date", "strength"}
        """
        student_date_superset = self.__df_alter_len(trainee_performance_df[["student_name", "date"]],
                                                    multiply=relation_multiplicity)
        strength_list = [self.faker.word() for _ in range(relation_multiplicity ** 2)]
        data = {
            "strength": lambda: random.choice(strength_list)
        }
        dtypes = {
            "strength": self.dt['object'].dtype
        }
        return self.__df_builder(data, dtypes, len(student_date_superset.index), join_df=student_date_superset[["student_name", "date"]])

    def _get_tech_self_score_junction_df(self, trainee_performance_df: pd.DataFrame, *, relation_multiplicity: int = 5) -> pd.DataFrame:
        """
        columns: {"student_name", "date", "tech_self_score", "value"}
        """
        student_date_superset = self.__df_alter_len(trainee_performance_df[["student_name", "date"]],
                                                    multiply=relation_multiplicity)
        tech_self_score_list = [self.faker.word() for _ in range(relation_multiplicity ** 2)]
        data = {
            "tech_self_score": lambda: random.choice(tech_self_score_list),
            "value": lambda: random.randint(1, 10)
        }
        dtypes = {
            "tech_self_score": self.dt['object'].dtype,
            "value": self.dt['int'].dtype
        }
        return self.__df_builder(data, dtypes, len(student_date_superset.index), join_df=student_date_superset[["student_name", "date"]])

    def _get_test_score_df(self) -> pd.DataFrame:
        """
        columns: {"student_name", "date", "psychometrics", "presentations"}
        """
        data = {
            "psychometrics": lambda: f"{str(random.randint(0, 100))}/100",
            "presentations": lambda: f"{str(random.randint(0, 32))}/32"
        }
        dtypes = {
            "psychometrics": self.dt['object'].dtype,
            "presentations": self.dt['object'].dtype
        }
        return self.__df_builder(data, dtypes, len(self.student_date_df.index), join_df=self.student_date_df)

    def fake_transform_academy_csv(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        trainer_df {"trainer_name"}
        course_df {"course_name", "trainer_name", "date"}
        academy_performance_df {"student_name", "date", "course_name", "week", "analytic", "independent", "determined",
        "professional", "studious", "imaginative"}
        """
        trainer_df = self._get_trainer_df(int(self.no_of_students / 10))
        self.course_df = self._get_course_df(trainer_df)
        academy_performance_df = self._get_academy_performance_df(self.course_df)
        return trainer_df, self.course_df, academy_performance_df

    def fake_transform_talent_csv(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        student_information_df {"student_name", "date", "gender", "dob", "email", "city", "address", "postcode",
        "phone_number", "uni", "degree"}
        invitation_df {"student_name", "date", "invited_date", "invited_by"}
        """
        student_information_df = self._get_student_information_df()
        invitation_df = self._get_invitation_df()
        return student_information_df, invitation_df

    def fake_transform_talent_json(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        trainee_performance_df {"student_name", "date", "self_development", "geo_flex", "financial_support", "result",
        "course_interest"}
        weakness_junction_df {"student_name", "date", "weakness"}
        strength_junction_df {"student_name", "date", "strength"}
        tech_self_score_junction_df {"student_name", "date", "tech_self_score", "value"}
        """
        trainee_performance_df = self._get_trainee_performance_df(self.course_df)
        weakness_junction_df = self._get_weakness_junction_df(trainee_performance_df)
        strength_junction_df = self._get_strength_junction_df(trainee_performance_df)
        tech_self_score_junction_df = self._get_tech_self_score_junction_df(trainee_performance_df)
        return trainee_performance_df, weakness_junction_df, strength_junction_df, tech_self_score_junction_df

    def fake_transform_talent_txt(self) -> pd.DataFrame:
        """
        test_score_df {"student_name", "date", "psychometrics", "presentations"}
        """
        return self._get_test_score_df()


if __name__ == "__main__":  # pragma: no cover
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)

    get_fake_df = GetFakeDf()
    _trainer_df, _course_df, _academy_performance_df = get_fake_df.fake_transform_academy_csv()
    _student_information_df, _invitation_df = get_fake_df.fake_transform_talent_csv()
    _trainee_performance_df, _weakness_junction_df, _strength_junction_df, _tech_self_score_junction_df = get_fake_df.fake_transform_talent_json()
    _test_score_df = get_fake_df.fake_transform_talent_txt()

    # print(f"trainer_df:\n{_trainer_df}\n")
    # print(f"course_df:\n{_course_df}\n")
    # print(f"academy_performance_df:\n{_academy_performance_df}\n")

    # print(f"student_information_df:\n{_student_information_df}")
    # print(f"invitation_df:\n{_invitation_df}")

    # print(f"trainee_performance_df:\n{_trainee_performance_df}")
    # print(f"weakness_junction_df:\n{_weakness_junction_df}")
    # print(f"strength_junction_df:\n{_strength_junction_df}")
    # print(f"tech_self_score_junction_df:\n{_tech_self_score_junction_df}")

    # print(f"test_score_df:\n{_test_score_df}")
