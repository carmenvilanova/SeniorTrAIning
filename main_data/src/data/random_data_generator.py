import random
import pandas as pd
import random

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

