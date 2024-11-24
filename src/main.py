import logging

from src.user_interaction import UserInteraction

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    UserInteraction.read_maze_params_and_gen_maze()


if __name__ == "__main__":
    main()
