import numpy as np

walls, blocked = (
    np.ones((3, 3, 4), dtype=bool),
    np.arange(9).reshape(3,3)
)


print(blocked)
print(blocked[2][2])
print(blocked[2,2])
