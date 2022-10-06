from .seed_db import SeedDB, many_to_many_relationship_generator
from ..models import TechScore, Strength, Weakness


def standard_factory() -> None:  # pragma: no cover
    seed = SeedDB()

    # generate some TechScore, Strength, Weakness entries
    for _ in range(10):
        seed.tech_score()
        seed.strength()
        seed.weakness()

    # generate some trainers and courses
    for _ in range(5):
        seed.trainer()
        seed.course()

    # generate some students with invitation, test score and academy performance data
    for _ in range(25):
        seed.invitation()
        seed.test_score()
        seed.academy_performance()
        seed.trainee_performance()
        seed.student_information()

    # build many-to-many relationships
    many_to_many_relationship_generator('tech_scores', TechScore, null=False)
    many_to_many_relationship_generator('strengths', Strength, null=False)
    many_to_many_relationship_generator('weaknesses', Weakness, null=False)
