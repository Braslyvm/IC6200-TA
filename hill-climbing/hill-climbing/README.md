# Hill Climbing

A hill climbing implementation for hospital placement optimization. The algorithm searches neighboring states and iteratively improves the map cost until reaching a local optimum.

## Functions

### utils.py

- `is_free_to_move(map, move)` - Checks if a target position is empty
- `is_valid_move(map, move)` - Checks if a position is inside map boundaries
- `find_objects(map, target_object_symbol)` - Returns coordinates of all matching objects
- `result(map, hospital_coordinates, target_move)` - Returns a new map after moving a hospital
- `manhattan(pos, pos_2)` - Computes Manhattan distance between two coordinates
- `cost(map)` - Returns total map cost (sum of hospital-house Manhattan distances)
- `move(pos, pos_2)` - Adds two coordinate tuples component-wise
- `actions(map, hospital_position)` - Returns all valid adjacent moves for a hospital

### hc.py

- `hill_climbing(map)` - Optimizes hospital positions using hill climbing until no better neighbor is found

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Run the Algorithm

### Quick run (default map)

This project includes a sample map in `main.py`. Run it with:

Windows:

```bash
python main.py
```

Linux/macOS:

```bash
python3 main.py
```

The script prints:

1. The original map.
2. The optimized map after applying the hill-climbing algorithm.

### Run with your own map (Python snippet)

```python
import hc
import utils
from tabulate import tabulate

custom_map = [
    [None, None, utils.OBJECT_HOSPITAL, None],
    [utils.OBJECT_HOUSE, None, None, None],
    [None, None, None, utils.OBJECT_HOUSE],
]

solved_map = hc.hill_climbing(custom_map)
print(tabulate(solved_map, tablefmt="grid", floatfmt=".2f"))
```

## Testing

### Windows

Use `python -m pytest` on Windows.

Run all tests:

```bash
python -m pytest
```

Run a specific test file:

```bash
python -m pytest tests/test_utils.py
python -m pytest tests/test_hill_climbing.py
```

Run a specific test function:

```bash
python -m pytest tests/test_utils.py::test_function_name
```

Run tests matching a pattern:

```bash
python -m pytest -k "test_name"
```

Run without coverage (faster):

```bash
python -m pytest --no-cov
```

### Linux/macOS

You can run tests with:

```bash
pytest
```

## Contributing

Short contributions are welcome and appreciated.

1. Fork the repository.
2. Create a branch for your change.
3. Make your update and keep it focused.
4. Run tests before submitting:
   - Windows: `python -m pytest`
   - Linux/macOS: `pytest`
5. Open a Pull Request with a clear description of what and why.

Please keep PRs small, readable, and related to a single improvement.
