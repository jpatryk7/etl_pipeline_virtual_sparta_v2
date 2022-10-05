from .seed_db import SeedDB


def standard_factory() -> None:  # pragma: no cover
    seed = SeedDB()
    seed.trainer()
    seed.course()
    for _ in range(10):
        seed.invitation()
        seed.test_score()
        seed.academy_performance()
        seed.student_information()
