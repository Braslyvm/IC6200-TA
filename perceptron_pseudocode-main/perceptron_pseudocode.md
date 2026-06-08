# Pseudocode — Perceptron

## perceptron.py

### Data

```
degrees_fahrenheit ← [
    -20.0000, -8.4211, 3.1579, 14.7368, 26.3158,
    37.8947, 49.4737, 61.0526, 72.6316, 84.2105,
    95.7895, 107.3684, 118.9474, 130.5263, 142.1053,
    153.6842, 165.2632, 176.8421, 188.4211, 200.0000
]

degrees_celsius ← fahrenheit_to_celsius applied to each value in degrees_fahrenheit
```

---

### fahrenheit_to_celsius(f)

```
FUNCTION fahrenheit_to_celsius(f):
    RETURN (f - 32) * 5 / 9
```

### mean(elements)

```
FUNCTION mean(elements):
    IF elements is empty:
        RAISE error "Cannot compute mean of an empty list"

    total ← 0

    FOR each element in elements:
        total ← total + element

    RETURN total / number of elements
```

### standard_deviation(elements)

```
FUNCTION standard_deviation(elements):
    IF elements is empty:
        RAISE error "Cannot compute standard deviation of an empty list"

    mean_value ← mean(elements)
    variance ← average of (element - mean_value)^2 for each element

    RETURN square_root(variance)
```

---

## Normalize

### normalize(dataset)

```
FUNCTION normalize(dataset):
    value_hat ← mean(dataset)
    value_sd  ← standard_deviation(dataset)

    IF value_sd == 0:
        RAISE error "Cannot normalize values with zero standard deviation"

    value_norm ← empty list

    FOR each element in dataset:
        value ← (element - value_hat) / value_sd
        value_norm.append(value)

    RETURN value_norm
```

### denormalize(value, dataset)

```
FUNCTION denormalize(value, dataset):
    value_hat ← mean(dataset)
    value_sd  ← standard_deviation(dataset)

    // Inverse of normalization:
    // original_value = normalized_value * standard_deviation + mean
    RETURN value * value_sd + value_hat
```

### Normalized Datasets

```
x_normalized ← normalize(degrees_fahrenheit)
y_normalized ← normalize(degrees_celsius)
```

---

## Train

### Perceptron Formula

```
The base perceptron formula is:

    y_hat = activation(w · x + b)

Where:
    w · x = w1*x1 + w2*x2 + ... + wn*xn

For this single-input linear perceptron:
    y_hat = w * x + b

Meaning:
    x = input value / feature
    w = weight
    b = bias
    y_hat = predicted output
```

### perceptron(x, w, b)

```
FUNCTION perceptron(x, w, b):
    // Linear model / single-input perceptron
    // y_hat = w * x + b
    RETURN w * x + b
```

### train_perceptron(x_values, y_values, w, b, learning_rate, epochs)

```
FUNCTION train_perceptron(x_values, y_values, w, b, learning_rate, epochs):
    IF length of x_values != length of y_values:
        RAISE error "x_values and y_values must have the same length"

    IF x_values is empty:
        RAISE error "Cannot train with an empty dataset"

    n ← length of x_values

    training_history ← {
        epochs:  empty list,
        weights: empty list,
        biases:  empty list,
        mse:     empty list
    }

    FOR epoch FROM 0 TO epochs - 1:
        dw  ← 0
        db  ← 0
        mse ← 0

        FOR each pair (x, y) from x_values and y_values:
            // Predict output with the current weight and bias
            y_hat ← perceptron(x, w, b)

            // Error / residual
            error ← y - y_hat

            // Mean Squared Error contribution
            mse ← mse + error^2

            // Accumulate gradient terms
            dw ← dw + x * error
            db ← db + error

        // Final MSE for this epoch
        mse ← mse / n

        // Partial derivative of MSE with respect to w
        d_mse_dw ← (-2 / n) * dw

        // Partial derivative of MSE with respect to b
        d_mse_db ← (-2 / n) * db

        // Gradient descent update rule
        w ← w - learning_rate * d_mse_dw
        b ← b - learning_rate * d_mse_db

        training_history["epochs"].append(epoch + 1)
        training_history["weights"].append(w)
        training_history["biases"].append(b)
        training_history["mse"].append(mse)

        PRINT "Epoch", epoch + 1, "w=", w, "b=", b, "mse=", mse

    RETURN w, b, training_history
```

---

## Main Program

### Train and Predict

```
IF this file is run directly:
    w ← 0
    b ← 0

    learning_rate ← 0.3
    epochs ← 8

    mean_value ← mean(x_normalized)
    sd_value   ← standard_deviation(x_normalized)

    PRINT mean_value, sd_value

    w, b, training_history ← train_perceptron(
        x_normalized,
        y_normalized,
        w,
        b,
        learning_rate,
        epochs
    )

    PRINT "Final weight:", w
    PRINT "Final bias:", b

    fahrenheit_value ← -20
    fahrenheit_normalized ← (
        fahrenheit_value - mean(degrees_fahrenheit)
    ) / standard_deviation(degrees_fahrenheit)

    predicted_celsius_normalized ← perceptron(fahrenheit_normalized, w, b)
    predicted_celsius ← denormalize(predicted_celsius_normalized, degrees_celsius)

    PRINT "Predicted normalized Celsius:", predicted_celsius_normalized
    PRINT "Predicted Celsius:", predicted_celsius
```



