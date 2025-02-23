import random
import pandas as pd
import random

random.seed(123)

def generate_dni():
    """
    This function generates a valid Spanish DNI number. The Spanish DNI format consists of 8 random digits
    followed by a letter that is calculated based on the "Modulo 23" of the digits.

    The function ensures that the generated DNI number follows the official format, consisting of:
    - 8 digits (random number between 10000000 and 99999999)
    - 1 letter (calculated using the "Modulo 23" of the number)

    Returns:
    str: A valid Spanish DNI number in the format 'XXXXXXXXX' (8 digits + 1 letter).
    """

    # 8 random digits between 10000000 and 99999999
    number = random.randint(10000000, 99999999)
    
    # List of letters corresponding to the DNI number "Modulo 23"
    letters = "TRWAGMYFPDXBNJZSQVHLCKE"
    
    # Calculate letter by using the "Modulo 23" of the number
    letter = letters[number % 23]
    
    # Return the full DNI number as a string (8 digits + letter)
    return f"{number}{letter}"


def generate_dni_list(df: pd.DataFrame):
    """
    This function generates a list of unique DNI numbers (Spain) and replaces the 'ID' column in the provided DataFrame
    with these DNI numbers. The DNI format consists of 8 digits followed by a letter.

    Args:
    df (pd.DataFrame): The DataFrame where the 'ID' column will be replaced with unique DNI numbers.

    Returns:
    pd.DataFrame: The DataFrame with the 'ID' column replaced by unique DNI numbers.
    """
    # Generate a set of unique DNI numbers for each row in the DataFrame
    dni_set = set()
    dni_list = []
    
    for _ in range(len(df)):
        # Ensure unique DNI numbers
        while True:
            dni = generate_dni()
            if dni not in dni_set:
                dni_set.add(dni)
                dni_list.append(dni)
                break

    # Replace the 'ID' column with the generated DNI numbers
    df['ID'] = dni_list

    return df

def change_id_to_autoincrement(df, id_column='ID'):
    """
    Change the ID column to a numeric column which is auto-incrementable.
    
    Parameters:
    df (pd.DataFrame): The dataframe containing the ID column.
    id_column (str): The name of the ID column to be changed. Default is 'ID'.
    
    Returns:
    pd.DataFrame: The dataframe with the updated ID column.
    """
    df[id_column] = range(1, len(df) + 1)
    return df

import numpy as np

def estimate_languages_spoken(age: float, education_level: str) -> str:
    """
    Estimates how many languages ​​a person speaks based on their age and education level.
    Returns '1', '2', or '3+' depending on the assigned probability.

    Parameters:
    - age (float): Age of the person.
    - education_level (str): Education level ('University', 'High School', 'Primary School').

    Returns:
    - str: Estimated number of languages ​​spoken ('1', '2', or '3+').
    """
    random.seed(123)

    # Definir probabilidades base para cada edad
    if age < 30:
        probs = [0.1,  00.4,.5]  # 10% chance of speaking only 1 language, 40% chance of speaking 2 languages, 50% chance of speaking 3 or more
    elif age < 50:
        probs = [0.3, 0.5, 0.2] # More likely to speak 1 or 2 languages, less likely to speak 3+
    elif age < 70:
        probs = [0.5, 0.4, 0.1] # Greater likelihood of speaking only 1 language
    else:
        probs = [0.7, 0.25, 0.05]  # 70% chance of speaking only 1 language, only 5% chance of speaking 3 or more
    
    # Adjustment for educational level
    if education_level == 'University':
        # Subtract 0.2 from the probability of speaking only 1 language
        # Add 0.1 to the probability of speaking 2 languages
        # Add 0.1 to the probability of speaking 3 or more languages
        probs = [p + adj for p, adj in zip(probs, [-0.2, 0.1, 0.1])] 

    elif education_level == 'High School':
        # Subtract 0.1 to the probability of speaking only 1 language
        # Add 0.1 from the probability of speaking 2 languages
        # Add 0.1 from the probability of speaking 3 or more languages
        probs = [p + adj for p, adj in zip(probs, [-0.1, 0.1, 0.1])]
    
    elif education_level == 'Primary School':
        # Add 0.2 to the probability of speaking only 1 language
        # Subtract 0.1 from the probability of speaking 2 languages
        # Subtract 0.1 from the probability of speaking 3 or more languages
        probs = [p + adj for p, adj in zip(probs, [0.2, -0.1, -0.1])]
    
    # Ensure that the probabilities add up to 1
    probs = np.clip(probs, 0, 1) # Ensures that each probs value is in the range [0, 1]
    probs /= probs.sum() # Normalize the probabilities by dividing each value by the total sum of probs
    
    return np.random.choice(['1', '2', '3+'], p=probs)


def generate_reaction_time(age: float, education_level: str):

    random.seed(123)

    # Define influence of age
    if age <= 30: 
        coef = 0.01 
    elif age > 30 and age <= 50: 
        coef = 0.02 
    elif age > 50 and age <= 60:
        coef = 0.025
    elif age > 60 and age <= 70:
        coef = 0.035
    else :
        coef = 0.045
    
    # Adjust for education level
    if education_level == "University": 
        intercept = 1

    elif education_level == 'High School':
        intercept = 1.5
    
    elif education_level == 'Primary School':
        intercept = 2


    # Add error
    noise_e = np.random.normal(size=1)

    # Estimate reaction time
    react_time = 0.1 * ((coef*age) + (coef*age*age) + intercept + noise_e)
    return(react_time[0])

def generate_accuracy(age, education_level): 

    random.seed(123)

    # Define influence of age
    if age <= 30: 
        probs = [0.1, 0.15, .25, 0.5] 
    elif age > 30 and age <= 50: 
        probs = [0.15, 0.2, 0.3, 0.35] 
    elif age > 50 and age <= 60:
        probs = [0.2, 0.25, 0.35, 0.2]
    elif age > 60 and age <= 70:
        probs = [0.2, 0.35, 0.35, 0.1]
    else :
        probs = [0.25, 0.4, 0.25, .1]


    # Adjust for education level
    if education_level == "University": 
        probs = [p + adj for p, adj in zip(probs, [-0.05, -0.05, 0.1, 0.1])] 

    elif education_level == 'High School':
        probs = [p + adj for p, adj in zip(probs, [0.5, 0.05, -0.1, -0.15])] 
    
    elif education_level == 'Primary School':
        probs = [p + adj for p, adj in zip(probs, [0.08, 0.08, -0.15, -0.2])] 

    # Ensure that the probabilities add up to 1
    probs = np.clip(probs, 0, 1) # Ensures that each probs value is in the range [0, 1]
    probs /= probs.sum() # Normalize the probabilities by dividing each value by the total sum of probs
    
    # Generate random intervals of accuracy
    acc_list = [random.uniform(0, 0.2), random.uniform(0.15, 0.45), random.uniform(0.3, 0.75), random.uniform(0.5, 1)]

    # Select interval
    return np.random.choice(acc_list, p=probs)


def generate_cog_state(time, accuracy, time_ref, accuracy_ref):
    
    random.seed(123)

    if time > time_ref and accuracy < accuracy_ref: 
        probs = [0.75, 0.15, 0.1]
    elif time > time_ref and accuracy > accuracy_ref:
        probs = [0.6, 0.3, 0.1]
    elif time < time_ref and accuracy > accuracy_ref:
        probs = [0.05, 0.2, 0.75]
    else: # time < time_ref and accuracy < accuracy_ref
        probs = [0.1, 0.25, 0.65]

    return(np.random.choice(["Bajo", "Medio", "Alto"], p=probs)) # Cog. levels

