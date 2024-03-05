
from zenml.steps import Output, step
import secrets


@step(enable_cache=False)
def get_random_int() -> Output(random_num=int):
    """Get a random integer between 0 and 10."""
    return secrets.SystemRandom().randint(0, 10)
