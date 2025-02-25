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
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score, balanced_accuracy_score, roc_auc_score, confusion_matrix,roc_curve, auc, ConfusionMatrixDisplay
from sklearn.utils.class_weight import compute_class_weight

def logistic_regression_game01(data: pd.DataFrame, score_target: str, cog_level_importance: int):
    # Load data
    main_data = data  
    main_data["cog_level"].value_counts()  # Check

    # Encode target variable
    main_data["cog_level"] = main_data["cog_level"].replace({"Bajo": 0, "Medio": 1, "Alto": 2})
    main_data["cog_level"].value_counts()  # Check

    # Define X and y
    X = main_data[["age", "education_level", "languages_spoken", "gender", "average_time", "accuracy"]]
    y = main_data["cog_level"]

    # Reduce rare gender categories
    X["gender"] = X["gender"].replace({
        "Polygender": "Other", "Genderqueer": "Other", "Genderfluid": "Other",
        "Non-binary": "Other", "Agender": "Other", "Bigender": "Other"
    })

    # One-hot encoding for categorical variables
    X = pd.get_dummies(X, columns=["education_level", "gender", "languages_spoken"], drop_first=True)
    
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123)

    # Scaling function with weight adjustments
    def scale_vars(df, col_names, weights=None):
        scaler = StandardScaler()
        df[col_names] = scaler.fit_transform(df[col_names])
        
        # Apply weight adjustment if provided
        if weights:
            for col, weight in weights.items():
                df[col] *= weight
        
        return df

    # Define variable weights to increase their importance
    variable_weights = {"accuracy": 2.0, "average_time": 1.5, "age": 1.2}

    # Scale with weights
    X_train_sc = scale_vars(X_train, col_names=["age", "accuracy", "average_time"], weights=variable_weights)
    X_test_sc = scale_vars(X_test, col_names=["age", "accuracy", "average_time"], weights=variable_weights)

    # Define parameter grid
    params = {
        "C": [0.01, 0.05, 0.1, 0.2, 0.5, 1],
        "class_weight": ["balanced"]
    }

    scoring_metrics = ["accuracy", "precision", "recall", "balanced_accuracy", "roc_auc"]

    # Train model
    logit_model = LogisticRegression(random_state=123, multi_class="multinomial", fit_intercept=True)
    model = GridSearchCV(estimator=logit_model, cv=4, param_grid=params, refit=score_target, scoring=scoring_metrics)
    model.fit(X_train_sc, y_train)

    # Get best model and evaluate
    best_model = model.best_estimator_
    best_model.fit(X_train_sc, y_train)

    preds = best_model.predict(X_test_sc)

    # Compute evaluation metrics
    accuracy = accuracy_score(y_test, preds)
    recall = recall_score(y_test, preds, average="weighted")
    f1 = f1_score(y_test, preds, average="weighted")

    # Confusion Matrix
    cm = confusion_matrix(y_test, preds, labels=model.classes_)
    cm_disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
    cm_disp.plot()
    plt.show()

    print(f"Accuracy: {accuracy}")
    print(f"Recall: {recall}")
    print(f"F1 Score: {f1}")

    # Save the trained model
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../models/modelo.pkl"))
    joblib.dump(best_model, model_path)

    
    return best_model
