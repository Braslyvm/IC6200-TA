import math


# Implement the pseudocode
def fahrenheit_to_celsius(f):
    return (f - 32) * 5.0/9.0

degrees_fahrenheit = [
    -20.0000, -8.4211, 3.1579, 14.7368, 26.3158,
    37.8947, 49.4737, 61.0526, 72.6316, 84.2105,
    95.7895, 107.3684, 118.9474, 130.5263, 142.1053,
    153.6842, 165.2632, 176.8421, 188.4211, 200.0000
]
degrees_celsius = [
    fahrenheit_to_celsius(f) for f in degrees_fahrenheit
]   



def mean(elements):
    if len(elements)== 0:
        raise ValueError("Cannot compute mean of an empty list")
    total= 0 
    for x in elements:
        total +=x
    return total / len(elements)

def standard_deviation(elements):
    if len(elements)== 0:
        raise ValueError("Cannot compute standard deviation of an empty list")

    mean_value = mean(elements)
    variance = 0
    for x in elements:
        variance += (x - mean_value) ** 2
    return math.sqrt(variance / len(elements))
def normalize(dataset):
    value_hat= mean(dataset)
    value_sd = standard_deviation(dataset)
    if value_sd == 0 :
        raise ValueError("Cannot normalize values with zero standard deviation")
    
    value_norm= []
    for x in dataset:
        value = (x-value_hat)/value_sd
        value_norm.append(value)
    return value_norm

def denormalize(value,dataset):
    value_hat = mean(dataset)
    value_sd = standard_deviation(dataset)
    return value * value_sd + value_hat

x_normalized = normalize(degrees_fahrenheit)
y_normalized = normalize(degrees_celsius)


"""The base perceptron formula is:

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
"""
def perceptron(x,w,b):
    return w*x+b


def train_perceptron(x_values, y_values, w, b, learning_rate, epochs):
    if len(x_values) != len(y_values):
        raise ValueError("Input and output datasets must have the same length")
    if len(x_values) == 0:
        raise ValueError("Cannot train with an empty dataset")
    n = len(x_values)
    training_history = {
        "epochs": [],
        "weights": [],
        "biases": [],
        "mse": []
    }
    for epoch in range(epochs):
        dw  = 0
        db  = 0
        mse = 0
        for (x,y) in zip(x_values, y_values):
            y_hat = perceptron(x,w,b)
            error = y - y_hat
            mse += error ** 2
            dw += x * error
            db += error
            
        mse = mse / n
        d_mse_dw = (-2/n) * dw
        d_mse_db = (-2/n) * db
        w = w - learning_rate * d_mse_dw
        b = b - learning_rate * d_mse_db
        training_history["epochs"].append(epoch+1)
        training_history["weights"].append(w)
        training_history["biases"].append(b)
        training_history["mse"].append(mse)
        print(f"Epoch {epoch+1}: w={w:.4f}, b={b:.4f}, mse={mse:.4f}")
    return w, b, training_history


if __name__ == "__main__":
    w = 0.0
    b = 0.0
    learning_rate = 0.3
    epochs = 3
    mean(x_normalized)
    sd_x = standard_deviation(x_normalized)
    print(f"Mean of x_normalized: {mean(x_normalized):.4f}")
    w,b,training_history = train_perceptron(x_normalized, y_normalized, w, b, learning_rate, epochs)
    print(f"Final weights: w={w:.4f}")
    print(f"Final bias: b={b:.4f}")
    fahrenheit_test = -20.0
    fahrenheit_normalized = (fahrenheit_test - mean(degrees_fahrenheit)) / standard_deviation(degrees_fahrenheit)
    predicted_celsius_normalized = perceptron(fahrenheit_normalized, w, b)
    predicted_celsius = denormalize(predicted_celsius_normalized, degrees_celsius)
    print(f"Predicted normalized Celsius: {predicted_celsius_normalized:.4f}")
    print(f"Predicted Celsius: {predicted_celsius:.4f}")


