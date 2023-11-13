from tensorflow import keras
from keras import layers
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical

# Chargement des données MNIST

(X_train_digit, y_train_digit), (X_test_digit, y_test_digit) = keras.datasets.mnist.load_data()

'''print('trainset:', X_train_digit.shape)
print('testset:', X_test_digit.shape)'''

X_train_digit = X_train_digit / 255
X_test_digit = X_test_digit / 255

model_digit = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10)
])

model_digit.compile(optimizer='adam',
              loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model_digit.fit(X_train_digit, y_train_digit, epochs=5)

test_loss_digit, test_acc_digit = model_digit.evaluate(X_test_digit,  y_test_digit)
print('Test accuracy:', test_acc_digit)

train_data_letters = pd.read_csv('emnist-letters-train.csv', header=None)
test_data_letters = pd.read_csv('emnist-letters-test.csv', header=None)

# Divisez les données en caractéristiques (pixels) et étiquettes
X_train_letters = train_data_letters.iloc[:, 1:].values
y_train_letters = train_data_letters.iloc[:, 0].values

X_test_letters = test_data_letters.iloc[:, 1:].values
y_test_letters = test_data_letters.iloc[:, 0].values

# Redimensionnez les données
X_train_letters = X_train_letters.reshape(-1, 28, 28, 1)
X_test_letters = X_test_letters.reshape(-1, 28, 28, 1)

# Normalisez les valeurs des pixels
X_train_letters = X_train_letters.astype('float32') / 255.0
X_test_letters = X_test_letters.astype('float32') / 255.0

# Assurez-vous que les étiquettes sont en format one-hot encoding
num_classes = 27  # 27 lettres de l'alphabet plus une classe pour les caractères inconnus
y_train_letters = to_categorical(y_train_letters, num_classes)
y_test_letters = to_categorical(y_test_letters, num_classes)

# Séparation des données d'entraînement et de validation
X_train_letters, X_val, y_train_letters, y_val = train_test_split(X_train_letters, y_train_letters, test_size=0.2, random_state=42)

# Création du modèle CNN
model_letters = keras.Sequential([
    layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(27, activation='softmax')  # 26 classes pour les lettres de l'alphabet
])

# Compilation du modèle 
model_letters.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entraînement du modèle
model_letters.fit(X_train_letters, y_train_letters, epochs=5, validation_data=(X_val, y_val))

# Évaluer le modèle sur l'ensemble de test
test_loss_letters, test_acc_letters = model_letters.evaluate(X_test_letters, y_test_letters)
print(f'Test accuracy: {test_acc_letters}')