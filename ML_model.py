import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import os
import re
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import numpy as np



# Concatenate all DataFrames into one
combined_df = pd.read_csv('combined_sensor_data.csv')

# Handle missing values by forward filling and dropping remaining NaNs
combined_df_filled = combined_df.ffill().dropna()

# Selecting feature columns
X = combined_df_filled[['Light Intensity', 'Temperature', 'Soil Moisture', 'Humidity']]

# Selecting target variable columns
y = combined_df_filled[['Pump State', 'Fan State', 'Light State']]


# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Training a Decision Tree Classifier
decision_tree_model = DecisionTreeClassifier(random_state=42)
decision_tree_model.fit(X_train, y_train)

# Predicting on the test set
y_pred = decision_tree_model.predict(X_test)

# Calculating accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)


# Calculating accuracy for each state (column) individually
accuracy_pump_state = accuracy_score(y_test['Pump State'], y_pred[:, 0])
accuracy_fan_state = accuracy_score(y_test['Fan State'], y_pred[:, 1])
accuracy_light_state = accuracy_score(y_test['Light State'], y_pred[:, 2])

print("Accuracy for Pump State:", accuracy_pump_state)
print("Accuracy for Fan State:", accuracy_fan_state)
print("Accuracy for Light State:", accuracy_light_state)


# Data Visualization
# Histograms for each feature
combined_df_filled[['Light Intensity', 'Temperature', 'Soil Moisture', 'Humidity']].hist(figsize=(10, 8))
plt.show()

# Box plots for each feature
combined_df_filled[['Light Intensity', 'Temperature', 'Soil Moisture', 'Humidity']].plot(kind='box', subplots=True, layout=(2,2), figsize=(10, 8))
plt.show()

# Model Results Visualization
# Confusion matrices for each state
states = ['Pump State', 'Fan State', 'Light State']
for i, state in enumerate(states):
    cm = confusion_matrix(y_test[state], y_pred[:, i])
    sns.heatmap(cm, annot=True, fmt='d')
    plt.title(f'Confusion Matrix for {state}')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()

# # Feature Importance Plot
# feature_importances = decision_tree_model.feature_importances_
# sns.barplot(x=feature_importances, y=X.columns)
# plt.title('Feature Importances in Decision Tree')
# plt.xlabel('Importance')
# plt.ylabel('Feature')
# plt.show()

from sklearn.metrics import multilabel_confusion_matrix
import numpy as np

# Generating a multi-label confusion matrix
multi_label_cm = multilabel_confusion_matrix(y_test, y_pred)

# Flattening and concatenating the confusion matrices for each state
combined_cm = np.concatenate([cm.flatten() for cm in multi_label_cm]).reshape(3, 4)

# Creating labels for the axes
labels = ['TN', 'FP', 'FN', 'TP']
label_index = [f'{state} - {label}' for state in states for label in labels]

# Plotting the combined confusion matrix
sns.heatmap(combined_cm, annot=True, fmt='d', xticklabels=labels, yticklabels=states)
plt.title('Combined Confusion Matrix for All States')
plt.xlabel('Predicted Labels')
plt.ylabel('Actual States')
plt.show()
