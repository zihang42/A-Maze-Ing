import heapq

from ..utils import DIRECTIONS
from .utils import AlgorithmSolve, is_in_bound


class AstarSolve(AlgorithmSolve):
    def solve(self) -> list[tuple[int, int]]:
        def h(a: tuple[int, int], b: tuple[int, int]):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        priority_queue = []
        heapq.heappush(priority_queue, (0, self.entry))
        previous = {}
        g_cost = {self.entry: 0}
        visited = set()
        while priority_queue:
            _, curr = heapq.heappop(priority_queue)
            if curr in visited:
                continue
            visited.add(curr)
            if curr == self.exit:
                return self._path(previous)
            for neighbor in self._neighbors(curr):
                neighbor_g = g_cost[curr] + 1
                if neighbor_g < g_cost.get(neighbor, float("inf")):
                    previous[neighbor] = curr
                    g_cost[neighbor] = neighbor_g
                    f_score = neighbor_g + h(neighbor, self.exit)
                    heapq.heappush(priority_queue, (f_score, neighbor))
        return [self.entry]

    def _path(self, previous) -> list[tuple[int, int]]:
        path = []
        current = self.exit
        while current != self.entry:
            path.append(current)
            current = previous[current]
        path.append(self.entry)
        return path[::-1]

    def _neighbors(self, coord) -> list[tuple[int, int]]:
        row, col = coord
        neighbors = []
        for dr, dc, curr_wall, _ in DIRECTIONS:
            nr = row + dr
            nc = col + dc
            if not is_in_bound(self.grid, nr, nc):
                continue
            if self.grid.blocked[nr][nc]:
                continue
            if self.grid.walls[row][col][curr_wall]:
                continue
            neighbors.append((nr, nc))
        return neighbors
