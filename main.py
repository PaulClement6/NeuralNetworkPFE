import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons

X, y = make_moons(n_samples=100, noise=0.2)
X = X.T
y = y.reshape((1, y.shape[0]))
plt.scatter(X[0, :], X[1, :], c=y.reshape(y.shape[1],), cmap='bwr')

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def derivative_sigmoid(x):
    s = sigmoid(x)
    return s * (1 - s)

def initialisation(layer_dims):
    params = {}
    L = len(layer_dims)

    for l in range(1, L):
        params['W' + str(l)] = np.random.randn(layer_dims[l], layer_dims[l-1]) * np.sqrt(1. / layer_dims[l-1])
        params['b' + str(l)] = np.zeros((layer_dims[l], 1))

    return params

def forward_propagation(X, params):
    cache = {'A0': X}
    L = len(params) // 2

    for l in range(1, L+1):
        Z = params['W' + str(l)].dot(cache['A' + str(l-1)]) + params['b' + str(l)]
        cache['A' + str(l)] = sigmoid(Z)

    return cache

def compute_gradients(cache, y, params):
    m = y.shape[1]
    L = len(params) // 2

    dZ = cache['A' + str(L)] - y
    gradients = {}

    for l in reversed(range(1, L+1)):
        gradients['dW' + str(l)] = 1/m * np.dot(dZ, cache['A' + str(l-1)].T)
        gradients['db' + str(l)] = 1/m * np.sum(dZ, axis=1, keepdims=True)
        dZ = np.dot(params['W' + str(l)].T, dZ) * derivative_sigmoid(cache['A' + str(l-1)]) 

    return gradients

def backward_propagation(X, y, params, cache, learning_rate):
    gradients = compute_gradients(cache, y, params)

    L = len(params) // 2

    for l in range(1, L+1):
        params['W' + str(l)] = params['W' + str(l)] - learning_rate * gradients['dW' + str(l)]
        params['b' + str(l)] = params['b' + str(l)] - learning_rate * gradients['db' + str(l)]

    return params

def predict(X, params):
    cache = forward_propagation(X, params)
    L = len(params) // 2
    AL = cache['A' + str(L)]
    return AL >= 0.5

def visualisation(X, y, params):
    fig, ax = plt.subplots()
    ax.scatter(X[0, :], X[1, :], c=y.reshape(y.shape[1],), cmap='bwr', s=50)

    x_min, x_max = X[0, :].min() - 1, X[0, :].max() + 1
    y_min, y_max = X[1, :].min() - 1, X[1, :].max() + 1
    h = 0.01
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = predict(np.c_[xx.ravel(), yy.ravel()].T, params)
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap='bwr', alpha=0.3)
    plt.xlim(X[0, :].min(), X[0, :].max())
    plt.ylim(X[1, :].min(), X[1, :].max())

    plt.show()

def compute_cost(AL, y):
    m = y.shape[1]
    cost = -1/m * np.sum(y * np.log(AL + 1e-8) + (1-y) * np.log(1-AL + 1e-8))
    return cost

def neural_network(X, y, layer_dims, learning_rate=0.05, n_iter=10000):
    params = initialisation(layer_dims)

    for i in range(n_iter):
        cache = forward_propagation(X, params)
        params = backward_propagation(X, y, params, cache, learning_rate)

        # Optional: Print the learning rate, cost, and progress every 1000 iterations
        if i % 1000 == 0:
            AL = cache['A' + str(len(layer_dims) - 1)]
            cost = compute_cost(AL, y)
            print(f'Iteration {i}, Learning Rate: {learning_rate}, Cost: {cost}')

    y_pred = predict(X, params)
    visualisation(X, y, params)

    return y_pred

y_pred = neural_network(X, y, layer_dims=(X.shape[0], 32, 64, 64, 32, y.shape[0]), n_iter=10000)
