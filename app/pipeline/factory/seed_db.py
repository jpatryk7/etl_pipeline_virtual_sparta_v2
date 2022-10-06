from typing import Type, Union, Any
from faker import Faker
import random
from ..models import (
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


def many_to_many_relationship_generator(
        field_name: str,
        other_model: Type[Union[TechScore, Strength, Weakness]],
        *, null: bool = True,
        max_relations: int = 5) -> None:
    # list of all TraineePerformance objects and objects to connect to (e.g. all TechScore entries)
    trainee_performance_obj_all = list(TraineePerformance.objects.all())
    other_model_obj_all = list(other_model.objects.all())

    # restrict max number of other_object related to the TraineePerformance object
    if len(other_model_obj_all) < max_relations:
        max_relations = len(other_model_obj_all)

    # random number of relations to generate (e.g. if numbers are 5 and 8 then 5 TraineePerformance entries will
    # have a relation with 8 other_model entries)
    trainee_performance_no_of_relations = random.randint(1, len(trainee_performance_obj_all)) if null else len(trainee_performance_obj_all)
    other_model_no_of_relations = random.randint(1, max_relations)

    trainee_performance_subset = random.sample(trainee_performance_obj_all, trainee_performance_no_of_relations) if null else trainee_performance_obj_all
    other_model_subset = random.sample(other_model_obj_all, other_model_no_of_relations)

    for trainee_performance_obj in trainee_performance_subset:
        if field_name == "tech_scores":
            trainee_performance_obj.tech_scores.add(*other_model_subset)
        elif field_name == "strengths":
            trainee_performance_obj.strengths.add(*other_model_subset)
        elif field_name == "weaknesses":
            trainee_performance_obj.weaknesses.add(*other_model_subset)
        else:
            raise Exception(f"field_name must be 'tech_scores', 'strengths', 'weaknesses'. Got {field_name} instead.")


class IDManager:
    """
    Simple ID helper class to keep track of one-to-one relations
    """
    def __init__(self):
        self.available_ids = {
            'test_score_id': [],
            'invitation_id': [],
            'academy_performance_id': [],
            'trainee_performance_id': []
        }

    def add_id(self, field_name: str, _id: int) -> None:
        self.available_ids[field_name].append(_id)

    def remove_id(self, field_name: str, _id: int) -> None:
        self.available_ids[field_name].remove(_id)

    def get_random_id(self, field_name: str, remove: bool = True) -> int:
        random_id = random.choice(self.available_ids[field_name])
        if remove:
            self.remove_id(field_name, random_id)
        return random_id

    def get_ids(self, field_name: str) -> list[int]:
        return self.available_ids[field_name]


class SeedDB:  # pragma: no cover
    def __init__(self) -> None:
        self.faker = Faker('en_US')
        self.id_manager = IDManager()

    def student_information(self, *, null: bool = False) -> None:
        if null:
            university, degree, test_score_id, invitation_id, course_id, academy_performance_id, trainee_performance_id = (None, None, None, None, None, None, None)
        else:
            university = self.faker.text(max_nb_chars=10)
            degree = self.faker.text(max_nb_chars=10)

            course_id_all = Course.objects.all().values_list('id', flat=True)

            test_score_id = TestScore.objects.get(pk=self.id_manager.get_random_id('test_score_id'))
            invitation_id = Invitation.objects.get(pk=self.id_manager.get_random_id('invitation_id'))
            course_id = Course.objects.get(pk=random.choice(course_id_all))
            academy_performance_id = AcademyPerformance.objects.get(pk=self.id_manager.get_random_id('academy_performance_id'))
            trainee_performance_id = TraineePerformance.objects.get(pk=self.id_manager.get_random_id('trainee_performance_id'))

        student_information_obj = StudentInformation(
            name=self.faker.text(max_nb_chars=20),
            gender=self.faker.text(max_nb_chars=5),
            dob=self.faker.date(),
            email=self.faker.text(max_nb_chars=20),
            city=self.faker.text(max_nb_chars=20),
            address=self.faker.text(max_nb_chars=20),
            postcode=self.faker.text(max_nb_chars=5),
            university=university,
            degree=degree,
            test_score_id=test_score_id,
            invitation_id=invitation_id,
            course_id=course_id,
            academy_performance_id=academy_performance_id,
            trainee_performance_id=trainee_performance_id
        )

        student_information_obj.save()

    def trainee_performance(self, *, null: bool = False) -> None:
        if null:
            course_interest = None
        else:
            course_interest = self.faker.text(max_nb_chars=10)

        trainee_performance_obj = TraineePerformance(
            date=self.faker.date(),
            self_development=self.faker.boolean(),
            geo_flex=self.faker.boolean(),
            financial_support=self.faker.boolean(),
            course_interest=course_interest
        )

        trainee_performance_obj.save()

        # add many-to-many relationships
        tech_score_obj_all = TechScore.objects.all()
        tech_score_no_of_relations = random.randint(0, len(tech_score_obj_all))
        for i in range(tech_score_no_of_relations):
            trainee_performance_obj.tech_scores.add(tech_score_obj_all[i])

        # save id
        self.id_manager.add_id('trainee_performance_id', trainee_performance_obj.pk)

    def academy_performance(self, *, null: bool = False) -> None:
        if null:
            academy_performance_obj = AcademyPerformance(week=random.randint(1, 8))
        else:
            academy_performance_obj = AcademyPerformance(
                week=random.randint(1, 8),
                analytic=random.randint(1, 10),
                independent=random.randint(1, 10),
                determined=random.randint(1, 10),
                professional=random.randint(1, 10),
                studious=random.randint(1, 10),
                imaginative=random.randint(1, 10)
            )

        academy_performance_obj.save()
        self.id_manager.add_id('academy_performance_id', academy_performance_obj.pk)

    def course(self, *, null: bool = False) -> None:
        if null:
            trainer_id = None
        else:
            trainer_id_all = Trainer.objects.all().values_list('id', flat=True)
            trainer_id = Trainer.objects.get(pk=random.choice(trainer_id_all))

        course_obj = Course(
            week=random.randint(1, 8),
            course_name=self.faker.text(max_nb_chars=10),
            trainer_id=trainer_id
        )

        course_obj.save()

    def trainer(self) -> None:
        trainer_obj = Trainer(
            name=self.faker.text(max_nb_chars=20)
        )

        trainer_obj.save()

    def test_score(self) -> None:
        test_score_obj = TestScore(
            psychometrics=self.faker.text(max_nb_chars=10),
            presentation=self.faker.text(max_nb_chars=10)
        )

        test_score_obj.save()
        self.id_manager.add_id('test_score_id', test_score_obj.pk)

    def strength(self) -> None:
        strength_obj = Strength(strength=self.faker.text(max_nb_chars=5))

        strength_obj.save()

    def weakness(self) -> None:
        weakness_obj = Weakness(weakness=self.faker.text(max_nb_chars=5))

        weakness_obj.save()

    def invitation(self, *, null: bool = False) -> None:
        if null:
            date = None
        else:
            date = self.faker.date()

        invitation_obj = Invitation(
            date=date,
            invited_by=self.faker.text(max_nb_chars=20)
        )

        invitation_obj.save()
        self.id_manager.add_id('invitation_id', invitation_obj.pk)

    def tech_score(self) -> None:
        tech_score_obj = TechScore(
            tech_score_name=self.faker.text(max_nb_chars=10),
            value=random.randint(1, 10)
        )

        tech_score_obj.save()
