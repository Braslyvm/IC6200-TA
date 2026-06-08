# Perceptron

Temperature conversion from Fahrenheit to Celsius follows a simple linear relationship: subtract 32 from the Fahrenheit value, then multiply by 5/9. In this work, we use that relationship as a small learning problem for a single-input perceptron.

A perceptron receives an input value, multiplies it by a weight, adds a bias, and returns a prediction. For this project, the input is a Fahrenheit temperature and the target output is the equivalent Celsius temperature. The model starts with an initial weight and bias, then improves them over several training epochs by comparing predictions against the real Celsius values.

Because the Fahrenheit and Celsius values use different scales, the data is normalized before training. Normalization transforms each value based on the dataset mean and standard deviation, making training more stable. After the perceptron predicts a normalized Celsius value, that value can be denormalized back into the original Celsius scale.

During training, the perceptron calculates an error for each prediction, accumulates the mean squared error, and updates the weight and bias using gradient descent. The goal is for the learned weight and bias to approximate the Fahrenheit-to-Celsius relationship using the provided dataset.

For a high-level walkthrough of the logic, see [perceptron_pseudocode.md](perceptron_pseudocode.md).

## Functions

### perceptron.py

- `fahrenheit_to_celsius(f)` — Converts a Fahrenheit value into Celsius using `(f - 32) * 5 / 9`.
- `mean(elements)` — Computes the average value of a non-empty list.
- `standard_deviation(elements)` — Computes the population standard deviation of a non-empty list.
- `normalize(dataset)` — Converts dataset values into normalized values using the dataset mean and standard deviation.
- `denormalize(value, dataset)` — Converts a normalized value back to the original dataset scale.
- `perceptron(x, w, b)` — Returns the prediction `w * x + b` for a single input.
- `train_perceptron(x_values, y_values, w, b, learning_rate, epochs)` — Trains the perceptron by updating the weight and bias with gradient descent.

## Starter File

The current `perceptron.py` file is intentionally minimal:

```python
import math

# Implement the pseudocode
```

Use `perceptron_pseudocode.md` as the implementation guide.

## Usage

After implementing the pseudocode, run the program:

```bash
python perceptron.py
```

The program should train the perceptron, print training progress, and show a predicted Celsius value for a Fahrenheit input.

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Testing

Run all tests:

```bash
pytest
```

Run a specific test file:

```bash
pytest tests/test_utils.py
```

Run a specific test function:

```bash
pytest tests/test_utils.py::test_function_name
```

Run tests matching a pattern:

```bash
pytest -k "test_name"
```

Run without coverage, which is faster while developing:

```bash
pytest --no-cov
```
