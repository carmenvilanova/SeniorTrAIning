# Libreries
import sys
import os
import pandas as pd
import numpy as np
import random 
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression 
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score, confusion_matrix,roc_curve, auc, ConfusionMatrixDisplay

def logistic_regression_game01(data:pd.DataFrame):
    # Load data
    main_data = data # Acá debería ser el cargue del archivo de datos
    main_data["cog_level"].value_counts() # Check
    # Encode target variable
    main_data["cog_level"] = main_data["cog_level"].replace({"Bajo": 0, "Medio": 1, "Alto": 2})
    main_data["cog_level"].value_counts() # Check
    # Divide into train and test sets

    # --- Define X and y
    X = main_data[["age", "education_level", "languages_spoken", "gender", "average_time", "accuracy"]]
    y = main_data["cog_level"]

    # print(X[["education_level"]].value_counts())
    # print(X[["languages_spoken"]].value_counts())
    # print(X[["gender"]].value_counts())

    # --- Too few members for these categories
    X["gender"] = X["gender"].replace({"Polygender": "Other", "Genderqueer": "Other", "Genderfluid": "Other", 
                                    "Non-binary": "Other", "Agender": "Other", "Bigender": "Other"})

    # print(X["gender"].value_counts())

    # One hot encode categorical variables
    X = pd.get_dummies(X, columns=["education_level", "gender", "languages_spoken"])
    print(X.columns)
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 123)
    # Scale age, time and accuracy

    # --- Small helper function
    def scale_vars(df, col_names):

        for col_name in col_names:
            # Get mean and St. Dev
            x = df[col_name].mean()
            sd = df[col_name].std()

            # Scale
            df[col_name] = (df[col_name] - x)/sd
        
        return(df)

    # Scale
    X_train_sc = scale_vars(X_train, col_names=["age", "accuracy", "average_time"])
    X_test_sc = scale_vars(X_test, col_names=["age", "accuracy", "average_time"])

    # Define params grid and scoring metrics
    params = {
        "C": [0.1, 0.5, 1]
    }
    scoring_metrics = ["accuracy", "precision", "recall"]

    # Set model and train
    logit_model = LogisticRegression(random_state=123, fit_intercept=False) # Falso porque tenemos dummies para todas las categorías
    model = GridSearchCV(estimator=logit_model, cv=4, param_grid=params, refit="accuracy", scoring=scoring_metrics)
    model.fit(X_train_sc, y_train) 
    # Get best model and evaluate
    best_model = model.best_estimator_

    preds = best_model.predict(X_test_sc)
    # preds_proba = best_model.predict_proba(X_test) # To get probabilities for each class

    accuracy = accuracy_score(y_test, preds)
    recall = recall_score(y_test, preds, average="weighted")
    f1 = f1_score(y_test, preds, average="weighted")

    # print(f"Accuracy: {accuracy}")
    # print(f"Recall: {recall}")
    # print(f"F1: {f1}")
    # CM
    # print(confusion_matrix(y_test, preds, labels=model.classes_))

    # CM Heatmap
    cm = confusion_matrix(y_test, preds, labels=model.classes_)
    cm_disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
    cm_disp.plot()
    plt.show()
    # Guardar el modelo entrenado
    # joblib.dump(best_model, "../../modelo.pkl")

    # Define the new path of the trained model
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../models/modelo.pkl"))

    # Save the model
    joblib.dump(best_model, model_path)

    return best_model
