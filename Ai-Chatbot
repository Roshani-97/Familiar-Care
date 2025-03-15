import pandas as pd

def load_dataset(file_path):
    """Load the disease dataset."""
    return pd.read_excel(file_path)

def get_most_likely_disease(df, species, symptoms):
    """Find the disease with the most matching symptoms."""
    species_diseases = df[df['Animal'].str.lower() == species.lower()].copy()
    
    if species_diseases.empty:
        return None
    
    species_diseases['Match_Count'] = species_diseases['Symptoms'].apply(lambda x: sum(1 for symptom in symptoms if symptom.lower() in x.lower()))
    most_likely_disease = species_diseases.sort_values(by='Match_Count', ascending=False).iloc[0]
    
    return most_likely_disease if most_likely_disease['Match_Count'] > 0 else None

def provide_recommendation(disease_info):
    """Provide recommendations based on disease severity."""
    severity = disease_info['Severity']
    suggestions = disease_info['Suggestions']
    
    if severity.lower() == 'high':
        return f"The condition is severe. Please visit a vet immediately. Suggested care: {suggestions}"
    elif severity.lower() == 'moderate':
        return f"The condition is moderate. Consult a vet through video call or text. Suggested care: {suggestions}"
    else:
        return f"The condition is mild. You should still consult a vet. Here’s how you can help: {suggestions}"

def chatbot():
    """AI chatbot to diagnose pet diseases."""
    file_path = '/content/dti_ds_final_v4.xlsx'
    df = load_dataset(file_path)
    
    species = input("What species is your pet? ")
    symptoms = input("Enter the symptoms your pet is showing (comma-separated): ").split(', ')
    
    most_likely_disease = get_most_likely_disease(df, species, symptoms)
    
    if most_likely_disease is None:
        print("No matching diseases found. Please consult a vet.")
    else:
        print(f"Most likely disease: {most_likely_disease['Disease']}")
        print(provide_recommendation(most_likely_disease))

if __name__ == "__main__":
    chatbot()
