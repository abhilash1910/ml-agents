import pytest
from unittest.mock import patch, call, mock_open

from mlagents.trainers.meta_curriculum import MetaCurriculum
from mlagents.trainers.curriculum import Curriculum
from mlagents.trainers.exception import MetaCurriculumError

from mlagents.trainers.tests.test_simple_rl import (
    Simple1DEnvironment,
    _check_environment_trains,
    BRAIN_NAME,
)
from mlagents.trainers.tests.test_curriculum import dummy_curriculum_json_str


class MetaCurriculumTest(MetaCurriculum):
    """This class allows us to test MetaCurriculum objects without calling
    MetaCurriculum's __init__ function.
    """

    def __init__(self, brains_to_curriculums):
        self._brains_to_curriculums = brains_to_curriculums


@pytest.fixture
def default_reset_parameters():
    return {"param1": 1, "param2": 2, "param3": 3}


@pytest.fixture
def more_reset_parameters():
    return {"param4": 4, "param5": 5, "param6": 6}


@pytest.fixture
def measure_vals():
    return {"Brain1": 0.2, "Brain2": 0.3}


@pytest.fixture
def reward_buff_sizes():
    return {"Brain1": 7, "Brain2": 8}


@patch("mlagents.trainers.curriculum.Curriculum.get_config", return_value={})
@patch("mlagents.trainers.curriculum.Curriculum.__init__", return_value=None)
@patch("os.listdir", return_value=["Brain1.json", "Brain2.test.json"])
def test_init_meta_curriculum_happy_path(
    listdir, mock_curriculum_init, mock_curriculum_get_config, default_reset_parameters
):
    meta_curriculum = MetaCurriculum("test/")

    assert len(meta_curriculum.brains_to_curriculums) == 2

    assert "Brain1" in meta_curriculum.brains_to_curriculums
    assert "Brain2.test" in meta_curriculum.brains_to_curriculums

    calls = [call("test/Brain1.json"), call("test/Brain2.test.json")]

    mock_curriculum_init.assert_has_calls(calls)


@patch("os.listdir", side_effect=NotADirectoryError())
def test_init_meta_curriculum_bad_curriculum_folder_raises_error(listdir):
    with pytest.raises(MetaCurriculumError):
        MetaCurriculum("test/")


@patch("mlagents.trainers.curriculum.Curriculum")
@patch("mlagents.trainers.curriculum.Curriculum")
def test_set_lesson_nums(curriculum_a, curriculum_b):
    meta_curriculum = MetaCurriculumTest(
        {"Brain1": curriculum_a, "Brain2": curriculum_b}
    )

    meta_curriculum.lesson_nums = {"Brain1": 1, "Brain2": 3}

    assert curriculum_a.lesson_num == 1
    assert curriculum_b.lesson_num == 3


@patch("mlagents.trainers.curriculum.Curriculum")
@patch("mlagents.trainers.curriculum.Curriculum")
def test_increment_lessons(curriculum_a, curriculum_b, measure_vals):
    meta_curriculum = MetaCurriculumTest(
        {"Brain1": curriculum_a, "Brain2": curriculum_b}
    )

    meta_curriculum.increment_lessons(measure_vals)

    curriculum_a.increment_lesson.assert_called_with(0.2)
    curriculum_b.increment_lesson.assert_called_with(0.3)


@patch("mlagents.trainers.curriculum.Curriculum")
@patch("mlagents.trainers.curriculum.Curriculum")
def test_increment_lessons_with_reward_buff_sizes(
    curriculum_a, curriculum_b, measure_vals, reward_buff_sizes
):
    curriculum_a.min_lesson_length = 5
    curriculum_b.min_lesson_length = 10
    meta_curriculum = MetaCurriculumTest(
        {"Brain1": curriculum_a, "Brain2": curriculum_b}
    )

    meta_curriculum.increment_lessons(measure_vals, reward_buff_sizes=reward_buff_sizes)

    curriculum_a.increment_lesson.assert_called_with(0.2)
    curriculum_b.increment_lesson.assert_not_called()


@patch("mlagents.trainers.curriculum.Curriculum")
@patch("mlagents.trainers.curriculum.Curriculum")
def test_set_all_curriculums_to_lesson_num(curriculum_a, curriculum_b):
    meta_curriculum = MetaCurriculumTest(
        {"Brain1": curriculum_a, "Brain2": curriculum_b}
    )

    meta_curriculum.set_all_curriculums_to_lesson_num(2)

    assert curriculum_a.lesson_num == 2
    assert curriculum_b.lesson_num == 2


@patch("mlagents.trainers.curriculum.Curriculum")
@patch("mlagents.trainers.curriculum.Curriculum")
def test_get_config(
    curriculum_a, curriculum_b, default_reset_parameters, more_reset_parameters
):
    curriculum_a.get_config.return_value = default_reset_parameters
    curriculum_b.get_config.return_value = default_reset_parameters
    meta_curriculum = MetaCurriculumTest(
        {"Brain1": curriculum_a, "Brain2": curriculum_b}
    )

    assert meta_curriculum.get_config() == default_reset_parameters

    curriculum_b.get_config.return_value = more_reset_parameters

    new_reset_parameters = dict(default_reset_parameters)
    new_reset_parameters.update(more_reset_parameters)

    assert meta_curriculum.get_config() == new_reset_parameters


META_CURRICULUM_CONFIG = """
    default:
        trainer: ppo
        batch_size: 16
        beta: 5.0e-3
        buffer_size: 64
        epsilon: 0.2
        hidden_units: 128
        lambd: 0.95
        learning_rate: 5.0e-3
        max_steps: 100
        memory_size: 256
        normalize: false
        num_epoch: 3
        num_layers: 2
        time_horizon: 64
        sequence_length: 64
        summary_freq: 50
        use_recurrent: false
        reward_signals:
            extrinsic:
                strength: 1.0
                gamma: 0.99
    """


@pytest.mark.parametrize("curriculum_brain_name", [BRAIN_NAME, "WrongBrainName"])
def test_simple_metacurriculum(curriculum_brain_name):
    env = Simple1DEnvironment(use_discrete=False)
    with patch(
        "builtins.open", new_callable=mock_open, read_data=dummy_curriculum_json_str
    ):
        curriculum = Curriculum("TestBrain.json")
    mc = MetaCurriculumTest({curriculum_brain_name: curriculum})
    _check_environment_trains(env, META_CURRICULUM_CONFIG, mc, -100.0)
