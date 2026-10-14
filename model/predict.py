import pickle
import pandas as pd
# import the ml model
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

# ML Flow
MODEL_VERSION = '1.0.0'


def predict_output(user_input: dict):
    """
    Returns a dictionary with predicted category, confidence, and class probabilities
    """
    input_df = pd.DataFrame([user_input])
    
    # Get prediction
    prediction = model.predict(input_df)[0]
    
    # Get prediction probabilities
    try:
        probabilities = model.predict_proba(input_df)[0]
        class_names = model.classes_
        class_probabilities = {str(class_name): float(prob) for class_name, prob in zip(class_names, probabilities)}
        confidence = float(max(probabilities))
    except (AttributeError, TypeError):
        # If model doesn't have predict_proba, use prediction only
        class_probabilities = {str(prediction): 1.0}
        confidence = 1.0
    
    return {
        'predicted_category': str(prediction),
        'confidence': confidence,
        'class_probabilities': class_probabilities
    }