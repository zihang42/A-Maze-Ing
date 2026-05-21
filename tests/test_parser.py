from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from parser import ConfigModel, Parser
from src.utils import GenerateMethod


@pytest.fixture
def valid_data() -> dict[str, Any]:
    return {
        "WIDTH": 10,
        "HEIGHT": 10,
        "ENTRY": "0,1",
        "EXIT": "9,9",
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": True,
        "SEED": 42,
        "ALGORITHM": "backtracking",
        "DISPLAY_42": True,
    }


def test_valid_date(valid_data: dict[str, Any]) -> None:
    model = ConfigModel(**valid_data)
    assert model.width == 10
    assert model.height == 10
    assert model.entry == (0, 1)
    assert model.exit == (9, 9)
    assert model.output_file == "maze.txt"
    assert model.perfect is True
    assert model.seed == 42
    assert model.algorithm == GenerateMethod.BACKTRACKING
    assert model.display_42 is True


def test_same_entry_exit(valid_data: dict[str, Any]) -> None:
    valid_data["ENTRY"] = "0,0"
    valid_data["EXIT"] = "0,0"
    with pytest.raises(ValidationError) as info:
        ConfigModel(**valid_data)
    assert "entry and exit can't be the same!" in str(info.value)


def test_entry_exit_out_bound(valid_data: dict[str, Any]) -> None:
    valid_data["ENTRY"] = "12,2"
    valid_data["EXIT"] = "15,20"
    with pytest.raises(ValidationError):
        ConfigModel(**valid_data)


def test_valid_parser(tmp_path: Path) -> None:
    f = tmp_path / "valid_config.txt"
    content = """
# This a comment
WIDTH= 10
HEIGHT= 10
ENTRY= 0,1
EXIT= 9,9


OUTPUT_FILE= maze.txt
PERFECT= True
SEED= 42
ALGORITHM= backtracking
DISPLAY_42= True
"""
    f.write_text(content)
    parser = Parser(str(f))
    data = parser.parse()
    assert data["WIDTH"] == "10"
    assert data["SEED"] == "42"
    assert "# This a comment" not in data
    model = ConfigModel(**data)
    assert model.entry == (0, 1)
    assert model.exit == (9, 9)
    assert model.algorithm == GenerateMethod.BACKTRACKING
    assert model.display_42 is True
