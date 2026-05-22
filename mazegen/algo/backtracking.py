import random

from .utils import AlgorithmGen, is_blocked, is_in_bound, open_wall


class BacktrackingGen(AlgorithmGen):
    def generate(self) -> None:
        self._backtracking(self.start)

    def _backtracking(self, coord: tuple[int, int]) -> None:
        if is_blocked(self.grid, coord):
            return
        random.shuffle(self.direction)
        self.visited[coord[0], coord[1]] = True
        for move_row, move_col, curr_wall, target_wall in self.direction:
            target_row = move_row + coord[0]
            target_col = move_col + coord[1]
            if not is_in_bound(self.grid, target_row, target_col):
                continue
            if is_blocked(self.grid, (target_row, target_col)):
                continue
            if self.visited[target_row, target_col]:
                continue
            open_wall(self.grid, coord[0], coord[1], curr_wall)
            open_wall(self.grid, target_row, target_col, target_wall)
            self._backtracking((target_row, target_col))
