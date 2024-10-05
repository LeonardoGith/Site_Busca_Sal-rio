import pandas as pd
import random

# Module-level variable to store the DataFrame (initially set to None)
_cached_df = None

# Options for profession names and regions
professions = ["Analista de Sistemas", "Analista de Dados", "Programador VBA", "Programador Python"]
regions = ["São Paulo", "Rio de Janeiro", "Minas Gerais"]

# Function to generate random data for the DataFrame
def generate_profession_data(n=100):
    data = {
        "Profession Name": [random.choice(professions) for _ in range(n)],
        "Profession Region": [random.choice(regions) for _ in range(n)],
        "Salary": [random.randint(1000, 10000) for _ in range(n)]
    }
    return pd.DataFrame(data)

# Function to get or create the DataFrame
def get_dataframe():
    global _cached_df
    if _cached_df is None:
        # DataFrame doesn't exist, so we create it
        _cached_df = generate_profession_data()
        print("DataFrame created.")
    else:
        # Reuse the existing DataFrame
        print("Reusing existing DataFrame.")
    return _cached_df

# Function to calculate the average salary for a given region and profession
def calculate_average_salary(df, region, profession):
    # Filter the DataFrame based on the specified region and profession
    filtered_df = df[(df['Profession Region'] == region) & (df['Profession Name'] == profession)]
    
    # Calculate and return the mean salary
    if not filtered_df.empty:
        average_salary = filtered_df['Salary'].mean()
        return average_salary
    else:
        return None  # Return None if no data matches the criteria
    

# This code runs when you call or import the module
if __name__ == "__main__":
    df = get_dataframe()
    print(df.head())
