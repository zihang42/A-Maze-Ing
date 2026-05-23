from pathlib import Path
from typing import Any, Self

from pydantic import BaseModel, Field, field_validator, model_validator

from mazegen.algo.utils import GenerateMethod


class ConfigModel(BaseModel):
    width: int = Field(..., alias="WIDTH", gt=2)
    height: int = Field(..., alias="HEIGHT", gt=2)
    entry: tuple[int, int] = Field(..., alias="ENTRY")
    exit: tuple[int, int] = Field(..., alias="EXIT")
    output_file: str = Field(..., alias="OUTPUT_FILE")
    perfect: bool = Field(..., alias="PERFECT")
    seed: int = Field(default=42, alias="SEED", ge=0)
    algorithm: GenerateMethod = Field(
        default=GenerateMethod.BACKTRACKING, alias="ALGORITHM"
    )
    display_42: bool = Field(default=True, alias="DISPLAY_42")

    @field_validator("entry", "exit", mode="before")
    def parse_coord(cls, coord: str | tuple[int, int]) -> tuple[int, int]:
        if isinstance(coord, tuple):
            return coord
        if isinstance(coord, str):
            parts = coord.split(",")
            if len(parts) == 2:
                x_str, y_str = (part.strip() for part in parts)
            else:
                raise ValueError("coordinate must be x,y")
            if x_str.isdigit() and y_str.isdigit():
                x, y = int(x_str), int(y_str)
                return (y, x)
        raise ValueError("coordinate must be x,y")

    @model_validator(mode="after")
    def validate_coord(self) -> Self:
        def _in_bounds(coord: tuple[int, int]) -> bool:
            row, col = coord
            return 0 <= row < self.height and 0 <= col < self.width

        if self.entry == self.exit:
            raise ValueError("entry and exit can't be the same!")
        if not _in_bounds(self.entry):
            raise ValueError("entry can't be outside of the bound!")
        if not _in_bounds(self.exit):
            raise ValueError("exit can't be outside of the bound!")

        return self


class Parser:
    def __init__(self, path: str) -> None:
        self.path = Path(path)

    def parse(self) -> dict[str, Any]:
        if not self.path.is_file():
            raise FileNotFoundError
        if not self.path.suffix == ".txt":
            raise ValueError("config file is not a .txt file!")
        data = {}
        lines = self.path.read_text().splitlines()
        for lineno, line in enumerate(lines, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, sep, value = line.partition("=")
            if not sep:
                raise ValueError(f"{lineno}: expected KEY=VALUE format!")
            data[key.strip()] = value.strip()
        return data

    def to_config(self) -> ConfigModel:
        data = self.parse()
        return ConfigModel(**data)
