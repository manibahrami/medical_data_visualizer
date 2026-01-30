#the data base is named medical-examination.csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. Import the data from medical_examination.csv and assign it to the df variable.
# This function typically gets df as an argument in the FCC test environment,
# but for self-containment and direct execution, we load it here.
# For the actual FCC submission, you might not load it in these functions if it's
# already loaded and passed from the main test file.

def draw_cat_plot():
    # Load data
    df = pd.read_csv('medical_examination.csv')

    # 2. Add an overweight column to the data.
    # Calculate BMI: weight in kilograms / (height in meters)^2
    # height is in cm, so convert to meters (divide by 100)
    df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)
    # If BMI > 25, set overweight to 1, else 0
    df['overweight'] = (df['bmi'] > 25).astype(int)

    # 3. Normalize data by making 0 always good and 1 always bad.
    # If the value of cholesterol or gluc is 1, set the value to 0.
    # If the value is more than 1, set the value to 1.
    df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1)
    df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1)

    # 4. Draw the Categorical Plot
    # Create a DataFrame for the cat plot using pd.melt
    # Melt df to create df_cat with 'cardio' as id_vars
    # and specified value_vars.
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # Group and reformat the data in df_cat
    # Group by 'cardio', 'variable', 'value' and count the occurrences
    # Reset index to make 'total' a column for plotting.
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'])['value'].count().reset_index(name='total')

    # Convert the data into long format and create a chart
    # Use sns.catplot() to draw the categorical plot
    # 'col' parameter splits the plot by 'cardio'
    fig = sns.catplot(
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        data=df_cat,
        kind='bar',
        height=5, aspect=1
    )
    # Ensure proper layout
    fig.set_axis_labels("Features", "Total Count")
    fig.set_titles("Cardio = {col_name}")

    # Do not modify the next two lines
    fig.savefig('cat_plot.png') # Saves the plot to a file
    return fig


def draw_heat_map():
    # Load data (if not passed as argument, as per FCC typical structure)
    df = pd.read_csv('medical_examination.csv')

    # 10. Clean the data in the df_heat variable by filtering out the following patient segments that represent incorrect data:
    # diastolic pressure is higher than systolic (ap_lo <= ap_hi)
    # height is less than the 2.5th percentile
    # height is more than the 97.5th percentile
    # weight is less than the 2.5th percentile
    # weight is more than the 97.5th percentile

    # Make a copy to avoid modifying original df for subsequent operations if draw_heat_map is called after other functions
    df_heat = df.copy() 

    df_heat = df_heat[
        (df_heat['ap_lo'] <= df_heat['ap_hi']) &
        (df_heat['height'] >= df_heat['height'].quantile(0.025)) &
        (df_heat['height'] <= df_heat['height'].quantile(0.975)) &
        (df_heat['weight'] >= df_heat['weight'].quantile(0.025)) &
        (df_heat['weight'] <= df_heat['weight'].quantile(0.975))
    ]

    # 11. Calculate the correlation matrix and store it in the corr variable.
    # Exclude 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight' columns for correlation
    # or ensure they are numeric. Let's make sure all relevant columns are numeric.
    # Need to normalize cholesterol, gluc and add overweight here too for consistency with cat_plot
    # Re-apply transformations/additions from draw_cat_plot to df_heat if df is loaded fresh here
    
    # Recalculate or ensure these columns are present and correctly normalized/added in df_heat
    df_heat['bmi'] = df_heat['weight'] / ((df_heat['height'] / 100) ** 2)
    df_heat['overweight'] = (df_heat['bmi'] > 25).astype(int)
    df_heat['cholesterol'] = df_heat['cholesterol'].apply(lambda x: 0 if x == 1 else 1)
    df_heat['gluc'] = df_heat['gluc'].apply(lambda x: 0 if x == 1 else 1)

    # Calculate correlation matrix
    corr = df_heat.corr()

    # 12. Generate a mask for the upper triangle and store it in the mask variable.
    # np.triu returns the upper triangle of an array (including the diagonal).
    mask = np.triu(corr)

    # 13. Set up the matplotlib figure.
    fig, ax = plt.subplots(figsize=(12, 12))

    # 14. Plot the correlation matrix using sns.heatmap().
    sns.heatmap(
        corr,
        linewidths=1,       # Line width between cells
        annot=True,         # Annotate heatmap with data values
        fmt=".1f",          # Format annotation values to one decimal place
        ax=ax,              # Use the specified axes
        cmap='icefire',     # Color map (e.g., 'viridis', 'coolwarm', 'icefire')
        mask=mask,          # Apply the mask to hide the upper triangle
        square=True,        # Force cells to be square
        cbar_kws={'shrink': 0.8} # Shrink color bar for better fit
    )

    # Do not modify the next two lines
    fig.savefig('heatmap.png') # Saves the plot to a file
    return fig

# --- Example Usage (for local testing purposes, typically in main.py) ---
# This part of the code will only run if the script is executed directly (not imported as a module).
# For FreeCodeCamp submission, their test_module.py will call these functions.
if __name__ == "__main__":
    # You need medical_examination.csv in the same directory.
    # Download it from: https://raw.githubusercontent.com/freeCodeCamp/boilerplate-medical-data-visualizer/main/medical_examination.csv
    
    # Run cat plot function
    cat_figure = draw_cat_plot()
    plt.show(block=False) # Show without blocking, so heatmap can also be shown if desired
    
    # Run heat map function
    heat_figure = draw_heat_map()
