import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier,RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
from utils.A2_ML_utils import is_categorical, export_model



# Title of the app
st.title("Machine Learning on custom data-sets")

# Option to use a sample dataset
if st.checkbox('Use Example Superstore Dataset'):
    # Load the example dataset
    df = pd.read_csv('data_files/Superstore.csv', encoding='ISO-8859-1')  # Replace with the path to your dataset
else:
    # File upload
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        # Read the file
        df = pd.read_csv(uploaded_file)
    else:
        # Show a message when no file is uploaded
        st.write("Please upload a CSV file or use the example dataset.")
        df = None

if df is not None:
    st.write(df)

    numerical_columns = df.select_dtypes(include=['int', 'float']).columns.tolist()
    if len(numerical_columns) > 0:
        input_columns = st.multiselect("Select input columns", numerical_columns, default=numerical_columns[:-1])
        target_column = st.selectbox("Select target column", numerical_columns, index=len(numerical_columns)-1)

        if st.button("Train Model"):
            X = df[input_columns]
            y = df[target_column]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

            # Determine if target variable is categorical or continuous
            if is_categorical(y):
                # Train classification model
                model = RandomForestClassifier()
                model.fit(X_train, y_train)
                predictions = model.predict(X_test)
                accuracy = accuracy_score(y_test, predictions)
                st.write(f"Classification Accuracy: {accuracy}")
            else:
                # Train regression model
                model = RandomForestRegressor()
                model.fit(X_train, y_train)
                predictions = model.predict(X_test)
                mse = round(mean_squared_error(y_test, predictions),2)
                st.write(f"Regression Mean Squared Error: {mse}")

                # Adding save your model button
                if st.button("Save Model"):
                    export_model(model, 'model.pkl')
                    st.write("Model saved successfully.")


    else:
        st.write("No numerical columns available in the dataset.")

