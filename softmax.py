import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from keras.datasets import mnist
from sklearn.preprocessing import LabelBinarizer
from azureml.core import Workspace
from tqdm import tqdm
from azureml.core.authentication import InteractiveLoginAuthentication

ws = Workspace.get(name='neuralNetwork_IA_AR',
                      subscription_id='cc51fdd6-ccaa-4819-9ae9-76f82f7e9a13',
                      resource_group='neural_network')

interactive_auth = InteractiveLoginAuthentication()
ws = Workspace.from_config(path="config.json", auth=interactive_auth)

def softmax(Z):
  return np.exp(Z) / np.sum(np.exp(Z), axis=0)

def sigmoid(x):
  return 1 / (1 + np.exp(-x))

def derivative_sigmoid(x):
  return x * (1 - x)

def initialisation(layer_dims):
  params = {}
  L = len(layer_dims)

  for l in range(1, L):
    params['W' + str(l)] = np.random.randn(layer_dims[l], layer_dims[l-1]) / np.sqrt(layer_dims[l-1])
    params['b' + str(l)] = np.zeros((layer_dims[l], 1))

  return params

def forward_propagation(X, params):
  cache = {'A0': X}
  L = len(params) // 2

  for l in range(1, L):
    Z = params['W' + str(l)].dot(cache['A' + str(l-1)]) + params['b' + str(l)]
    cache['A' + str(l)] = sigmoid(Z)

  Z = params['W' + str(L)].dot(cache['A' + str(L-1)]) + params['b' + str(L)]
  cache['A' + str(L)]= softmax(Z)

  return cache

def compute_gradients(cache, y, params):
  m = y.shape[1]
  L = len(params) // 2

  dZ = cache['A' + str(L)] - y
  gradients = {}

  for l in reversed(range(1, L+1)):
    gradients['dW' + str(l)] = 1/m * np.dot(dZ, cache['A' + str(l-1)].T)
    gradients['db' + str(l)] = 1/m * np.sum(dZ, axis=1, keepdims=True)
    if l > 1:
      dZ = np.dot(params['W' + str(l)].T, dZ) * derivative_sigmoid(cache['A' + str(l-1)]) 

  return gradients

def backward_propagation(X, y, params, cache, learning_rate):
  gradients = compute_gradients(cache, y, params)
  L = len(params) // 2

  for l in range(1, L+1):
    params['W' + str(l)] -= learning_rate * gradients['dW' + str(l)]
    params['b' + str(l)] -= learning_rate * gradients['db' + str(l)]

  return params

def compute_cost(y_pred, y_true):
  m = y_true.shape[1]
  cost = -1/m * np.sum(y_true * np.log(y_pred))
  return cost

def neural_network(X_train, y_train, X_test, y_test, layer_dims, learning_rate=0.05, n_iter=10000):
    params = initialisation(layer_dims)
    L = len(params)//2
    costs_train = []
    costs_test = []
    learning_rates = []

    for i in tqdm(range(n_iter)):
        cache_train = forward_propagation(X_train, params)
        params = backward_propagation(X_train, y_train, params, cache_train, learning_rate)
        cost_train = compute_cost(cache_train['A' + str(L)], y_train)
        costs_train.append(cost_train)
        cache_test = forward_propagation(X_test, params)
        cost_test = compute_cost(cache_test['A' + str(L)], y_test)
        costs_test.append(cost_test)
        learning_rates.append(learning_rate)

        if i % 100 == 0:
            print(f"Train cost at iteration {i} is {cost_train}")
            print(f"Test cost at iteration {i} is {cost_test}")

    plt.plot(costs_train, label="Train cost")
    plt.plot(costs_test, label="Test cost")
    plt.ylabel('cost')
    plt.xlabel('iterations')
    plt.legend()
    plt.show()

    plt.subplot(1,2,2)
    plt.plot(learning_rates)
    plt.ylabel('learning rate')
    plt.xlabel('iterations')
    plt.show()

    final_cache_train = forward_propagation(X_train, params)
    y_pred_train = np.argmax(final_cache_train['A' + str(L)], axis=0)

    return params, y_pred_train

(train_X, train_y), (test_X, test_y) = mnist.load_data()

train_X = train_X.reshape((train_X.shape[0], -1)).T / 255.0
test_X = test_X.reshape((test_X.shape[0], -1)).T / 255.0
train_y = train_y.reshape((1, train_y.shape[0]))
test_y = test_y.reshape((1, test_y.shape[0]))

lb = LabelBinarizer()
train_y = lb.fit_transform(train_y.T).T
test_y = lb.transform(test_y.T).T

params, y_pred_train = neural_network(train_X, train_y, test_X, test_y, [784, 128, 128 ,10], learning_rate=0.05, n_iter=10000)


cache_test = forward_propagation(test_X, params)
cost_test = compute_cost(cache_test['A' + str(len(params)//2)], test_y)
print("Cost on the test set: ", cost_test)

cache_train = forward_propagation(train_X, params)
cost_train = compute_cost(cache_train['A' + str(len(params)//2)], train_y)
print("Cost on the training set: ", cost_train)

# Now that training is complete, generate predictions for test set
final_cache_test = forward_propagation(test_X, params)
y_pred_test = np.argmax(final_cache_test['A' + str(len(params)//2)], axis=0)

# Visualization - example for the first 10 samples of the test set
fig, axes = plt.subplots(2, 5, figsize=(100, 5))
axes = axes.ravel()

for i in np.arange(0, 100):
    axes[i].imshow(test_X[:, i].reshape(28,28), cmap='gray')
    axes[i].set_title(f"True: {np.argmax(test_y[:, i])} \nPredict: {y_pred_test[i]}")
    axes[i].axis('off')
plt.subplots_adjust(wspace=0.5)

plt.show()
