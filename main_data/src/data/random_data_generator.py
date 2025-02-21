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
