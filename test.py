import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Read the Excel file
file_path = 'Part_2_Analysis.xlsx'  # Replace with the actual file path
df = pd.read_excel(file_path)

# Step 2: Display the DataFrame to confirm the data
print(df)

# Step 3: Prepare data for boxplot
# Select the relevant trial columns
trials_data = df[['Trial 1 Result', 'Trial 2 Result', 'Trial 3 Result']]

# Step 4: Create a boxplot
plt.figure(figsize=(10, 6))  # Set the figure size
plt.boxplot([trials_data[col] for col in trials_data.columns], labels=trials_data.columns)

# Step 5: Add titles and labels
plt.title('Boxplot of Trials Results for Different Number of Clients')
plt.xlabel('Trials')
plt.ylabel('Number of Messages')

# Step 6: Show the boxplot
plt.show()
