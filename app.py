from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
from model.predict import predict_output,model, MODEL_VERSION

app = FastAPI()

# human readable        
@app.get('/')
def home():
    return{'message':'Insurance Premium Prediction API'}

# machine readable
@app.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model_loaded': model is not None 
    }

@app.post('/predict', response_model=PredictionResponse)
def predict_premium(data: UserInput):

    User_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    try:
        prediction_result = predict_output(User_input)
        return PredictionResponse(
            predicted_category=prediction_result['predicted_category'],
            confidence=prediction_result['confidence'],
            class_probabilities=prediction_result['class_probabilities']
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={'error': str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)





