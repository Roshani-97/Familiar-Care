import pandas as pd

# Load the dataset
file_path = "/content/Encyclopedia dataset.xlsx"  # Update the path if needed
df = pd.read_excel(file_path)

# Strip any leading/trailing spaces from column names
df.columns = df.columns.str.strip()

# Rename columns for consistency
df.rename(columns={"Do's": "Do", "Don'ts": "Dont"}, inplace=True)

# Display column names (for debugging)
print("Available Columns:", df.columns)

def get_animal_advice(breed_name):
    """Fetch and display pet care advice based on breed."""
    breed_name = breed_name.strip().lower()

    # Search for the breed in the dataset
    result = df[df["Breed"].str.lower() == breed_name]
    
    if result.empty:
        print("❌ No data found for this breed.")
    else:
        for _, row in result.iterrows():
            print(f"\n🔹 Advice for {row['Breed']} 🔹")
            print(f"✅ Do: {row['Do']}")
            print(f"❌ Don't: {row['Dont']}")
            print(f"🍖 Diet: {row['Diet']}")
            print(f"🌦 Seasonal Habits: {row['Seasonal Habits']}\n")

# User Input
user_input = input("Enter the breed name: ")
get_animal_advice(user_input)
