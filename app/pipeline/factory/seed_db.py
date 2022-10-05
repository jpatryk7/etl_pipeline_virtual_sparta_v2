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


class SeedDB:  # pragma: no cover
    def __init__(self) -> None:
        self.faker = Faker('en_US')

    def student_information(self, *, null: bool = False) -> None:
        if null:
            university, degree, test_score_id, invitation_id, course_id, academy_performance_id = (None, None, None, None, None, None)
        else:
            university = self.faker.text(max_nb_chars=10)
            degree = self.faker.text(max_nb_chars=10)

            test_score_id_all = TestScore.objects.all().values_list('id', flat=True)
            invitation_id_all = Invitation.objects.all().values_list('id', flat=True)
            course_id_all = Course.objects.all().values_list('id', flat=True)
            academy_performance_id_all = AcademyPerformance.objects.all().values_list('id', flat=True)

            test_score_id = TestScore.objects.get(pk=random.choice(test_score_id_all))
            invitation_id = Invitation.objects.get(pk=random.choice(invitation_id_all))
            course_id = Course.objects.get(pk=random.choice(course_id_all))
            academy_performance_id = AcademyPerformance.objects.get(pk=random.choice(academy_performance_id_all))

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
            academy_performance_id=academy_performance_id
        )

        student_information_obj.save()

    def trainee_performance(self, *, null: bool = False) -> None:
        if null:
            student_information_id, course_interest = (None, None)
        else:
            student_information_id_all = StudentInformation.objects.all().values_list('id', flat=True)
            student_information_id = StudentInformation.objects.get(pk=random.choice(student_information_id_all))

        trainee_performance_obj = TraineePerformance(
            student_information_id=student_information_id,
            date = self.faker.date(),
            self_development=self.faker.boolean(),
            geo_flex=self.faker.boolean(),
            financial_support=self.faker.boolean(),
            course_interest=self.faker.text(max_nb_chars=10)
        )

        trainee_performance_obj.save()

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
            name=self.faker.text(max_nb_chars=200)
        )

        trainer_obj.save()

    def test_score(self) -> None:
        test_score_obj = TestScore(
            psychometrics=self.faker.text(max_nb_chars=10),
            presentation=self.faker.text(max_nb_chars=10)
        )

        test_score_obj.save()

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

    def tech_score(self) -> None:
        tech_score_obj = TechScore(
            tech_score_name=self.faker.text(max_nb_chars=10),
            value=random.randint(1, 10)
        )

        tech_score_obj.save()
