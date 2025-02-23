import pandas as pd
from datetime import datetime

def calculate_age(df: pd.DataFrame, birth_date_column: str):
    """
    This function calculates the age of each person in the DataFrame based on their birthdate.
    The birthdate column is assumed to be in the format YYYY-MM-DD HH:MM:SS.

    Args:
    df (pd.DataFrame): The DataFrame containing the birthdate column.
    birth_date_column (str): The name of the column in the DataFrame that contains the birthdates.

    Returns:
    pd.DataFrame: The DataFrame with an additional 'Age' column containing the calculated age.
    """

    # Convert the birthdate column to datetime (this will automatically handle the format)
    df[birth_date_column] = pd.to_datetime(df[birth_date_column])

    # Get the current date
    current_date = datetime.today()

    # Calculate the age for each person
    df['age'] = df[birth_date_column].apply(lambda birthdate: current_date.year - birthdate.year - ((current_date.month, current_date.day) < (birthdate.month, birthdate.day)))

    return df
