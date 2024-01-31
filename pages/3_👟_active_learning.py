import streamlit as st
st.set_page_config(layout='centered')
from modAL.models import ActiveLearner
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_digits
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

# Load the MNIST dataset
digits = load_digits()
X_raw = digits.images
y_raw = digits.target
X_pool = X_raw.reshape((X_raw.shape[0], -1)) # Flatten the images for ML model
y_pool = np.array([None]*len(y_raw)) # Initialize a pool of None labels for active learning

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_pool, y_raw, test_size=0.2, random_state=42)

# Initialize a learner
learner = ActiveLearner(
    estimator=RandomForestClassifier(),
    X_training=X_pool[:10], y_training=y_raw[:10] # Start with a small set of labeled data
)

# Initialize a list to keep track of accuracy scores
if 'Accuracy Scores' not in st.session_state.keys():
    st.session_state['Accuracy Scores'] = []
    #add initial accuracy score
    y_pred = learner.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    st.session_state['Accuracy Scores'].append(accuracy)

# Define the function to update the model and calculate accuracy
def update_model(query_idx):
    user_label = st.session_state['label']
    learner.teach(X_train[query_idx].reshape(1, -1), np.array([int(user_label)]))
    y_pred = learner.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    st.session_state['Accuracy Scores'].append(accuracy)
    st.write(f"Model updated. Current accuracy: {accuracy:.2f}")

def plot_accuracy():
    iterations = list(range(len(st.session_state['Accuracy Scores'])))
    acc = st.session_state['Accuracy Scores']

    #Make to df
    df = pd.DataFrame({'iterations':iterations,'acc':acc})
    st.subheader('Test Accuracy Scores')
    st.line_chart(data=df,
                  x = 'iterations',
                  y = 'acc',
                  use_container_width=True)

def active_learning_cycle():
    # Query for new data
    query_idx, query_inst = learner.query(X_train)
    # Display the image using Matplotlib
    image = X_raw[query_idx].reshape(8, 8)
    fig, ax = plt.subplots(figsize=(2, 2))
    ax.imshow(image, cmap='gray')
    ax.axis('off')
    st.pyplot(fig)
    # Use radio buttons for label input
    st.write("Label this image:")
    with st.form(key='label_form'):
        label = st.radio(label="",
                         options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                         horizontal=True)
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state['label'] = label
            update_model(query_idx)

# Streamlit App Layout
st.title("Active Learning with MNIST Dataset")
col1, col2 = st.columns(2)

with col1:
    active_learning_cycle()

with col2:
    plot_accuracy()

