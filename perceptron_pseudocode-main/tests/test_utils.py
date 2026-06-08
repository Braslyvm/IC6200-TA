import pytest

from perceptron import (
    denormalize,
    fahrenheit_to_celsius,
    mean,
    normalize,
    perceptron,
    standard_deviation,
    train_perceptron,
)


@pytest.mark.parametrize(
    ("fahrenheit", "expected_celsius"),
    [
        (-20.0000, -28.888888888889),
        (-8.4211, -22.456166666667),
        (3.1579, -16.023388888889),
        (14.7368, -9.590666666667),
        (26.3158, -3.157888888889),
        (37.8947, 3.274833333333),
        (49.4737, 9.707611111111),
        (61.0526, 16.140333333333),
        (72.6316, 22.573111111111),
        (84.2105, 29.005833333333),
        (95.7895, 35.438611111111),
        (107.3684, 41.871333333333),
        (118.9474, 48.304111111111),
        (130.5263, 54.736833333333),
        (142.1053, 61.169611111111),
        (153.6842, 67.602333333333),
        (165.2632, 74.035111111111),
        (176.8421, 80.467833333333),
        (188.4211, 86.900611111111),
        (200.0000, 93.333333333333),
    ],
)
def test_fahrenheit_to_celsius_converts_dataset_values(fahrenheit, expected_celsius):
    assert fahrenheit_to_celsius(fahrenheit) == pytest.approx(expected_celsius)


def test_mean_raises_when_no_values():
    with pytest.raises(ValueError, match="empty list"):
        mean([])


@pytest.mark.parametrize(
    ("values", "expected_mean"),
    [
        ([1], 1),
        ([1, 2], 1.5),
        ([1, 2, 3], 2),
        ([1, 2, 3, 4], 2.5),
        ([1, 2, 3, 4, 5], 3),
    ],
)
def test_mean_returns_expected_value(values, expected_mean):
    assert mean(values) == expected_mean


def test_standard_deviation_raises_when_no_values():
    with pytest.raises(ValueError, match="empty list"):
        standard_deviation([])


@pytest.mark.parametrize(
    ("values", "expected_standard_deviation"),
    [
        ([1], 0),
        ([1, 2], 0.5),
        ([1, 2, 3], 0.816496580928),
        ([1, 2, 3, 4], 1.118033988750),
        ([1, 2, 3, 4, 5], 1.414213562373),
    ],
)
def test_standard_deviation_returns_expected_value(values, expected_standard_deviation):
    assert standard_deviation(values) == pytest.approx(expected_standard_deviation)


def test_normalize_raises_when_no_values():
    with pytest.raises(ValueError, match="empty list"):
        normalize([])


def test_normalize_raises_when_standard_deviation_is_zero():
    with pytest.raises(ValueError, match="zero standard deviation"):
        normalize([1])


@pytest.mark.parametrize(
    ("values", "expected_normalized"),
    [
        ([1, 2], [-1, 1]),
        ([1, 2, 3], [-1.224744871392, 0, 1.224744871392]),
        (
            [1, 2, 3, 4],
            [-1.341640786500, -0.447213595500, 0.447213595500, 1.341640786500],
        ),
        (
            [1, 2, 3, 4, 5],
            [-1.414213562373, -0.707106781187, 0, 0.707106781187, 1.414213562373],
        ),
    ],
)
def test_normalize_returns_expected_values(values, expected_normalized):
    assert normalize(values) == pytest.approx(expected_normalized)


def test_denormalize_returns_original_value_from_normalized_value():
    assert denormalize(1, [1, 2]) == pytest.approx(2)


@pytest.mark.parametrize(
    ("x", "w", "b", "expected_output"),
    [
        (1, 2, 3, 5),
        (2, 3, 4, 10),
        (0, 3, 4, 4),
    ],
)
def test_perceptron_returns_weighted_value_plus_bias(x, w, b, expected_output):
    assert perceptron(x, w, b) == expected_output


def test_train_perceptron_raises_when_lengths_do_not_match():
    with pytest.raises(ValueError, match="same length"):
        train_perceptron([1], [1, 2], 0, 0, 0.1, 1)


def test_train_perceptron_raises_when_no_values():
    with pytest.raises(ValueError, match="empty dataset"):
        train_perceptron([], [], 0, 0, 0.1, 1)


def test_train_perceptron_updates_weight_and_bias_after_one_epoch():
    w, b, training_history = train_perceptron([1, 2], [2, 4], 0, 0, 0.1, 1)

    assert w == pytest.approx(1)
    assert b == pytest.approx(0.6)
    assert training_history["epochs"] == [1]
    assert training_history["weights"] == pytest.approx([1])
    assert training_history["biases"] == pytest.approx([0.6])
    assert training_history["mse"] == pytest.approx([10])
