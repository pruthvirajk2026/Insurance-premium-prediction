# Insurance Premium Category Predictor

This project predicts an insurance premium category from a person's details. It includes a FastAPI backend that serves a trained model and a Streamlit web interface for entering details and viewing the prediction.

## Features

- Predicts an insurance premium category and confidence score.
- Returns probabilities for each predicted class.
- Derives BMI, age group, lifestyle risk, and city tier from the submitted details.
- Provides interactive API documentation through FastAPI.

## Project layout

```text
.
├── app.py                     # FastAPI application
├── frontend.py                # Streamlit interface
├── model/
│   ├── model.pkl              # Trained prediction model
│   └── predict.py             # Model loading and prediction
├── requirements.txt
└── schema/                    # Request/response validation and city tiers
```

## Setup

Run commands from the project directory (the directory containing `app.py`):

```bash
cd "Insurance premium prediction"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt streamlit requests
```

`streamlit` and `requests` are installed separately because they are used by the frontend but are not currently listed in `requirements.txt`.

## Run the application

Start the API in one terminal:

```bash
cd "Insurance premium prediction"
source .venv/bin/activate
python -m uvicorn app:app --host 127.0.0.1 --port 8088
```

Start the frontend in a second terminal:

```bash
cd "Insurance premium prediction"
source .venv/bin/activate
INSURANCE_API_URL=http://127.0.0.1:8088/predict \
  python -m streamlit run frontend.py --server.address 127.0.0.1 --server.port 8502
```

Open the Streamlit app at <http://127.0.0.1:8502/>. The frontend sends predictions to `http://127.0.0.1:8088/predict`.

The model file is loaded using a path relative to the project directory, so start the API with the project directory as the working directory.

## API

When the API is running on port 8088:

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | API welcome message |
| `GET` | `/health` | Reports API/model health and model version |
| `POST` | `/predict` | Predicts a premium category |
| `GET` | `/docs` | Interactive Swagger documentation |

Example prediction request:

```bash
curl -X POST http://127.0.0.1:8088/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "weight": 65,
    "height": 1.7,
    "income_lpa": 10,
    "smoker": false,
    "city": "Mumbai",
    "occupation": "private_job"
  }'
```

The response includes the predicted category, confidence, and class probabilities. For example:

```json
{
  "predicted_category": "Low",
  "confidence": 0.69,
  "class_probabilities": {
    "High": 0.01,
    "Low": 0.69,
    "Medium": 0.3
  }
}
```

The example probabilities are illustrative; actual predictions depend on the input and trained model.

### Input fields

| Field | Type | Notes |
| --- | --- | --- |
| `age` | integer | Greater than 0 and less than 120 |
| `weight` | number | In kilograms; must be greater than 0 |
| `height` | number | In meters; must be greater than 0 and less than 2.5 |
| `income_lpa` | integer | Annual income in lakhs per annum; must be greater than 0 |
| `smoker` | boolean | `true` or `false` |
| `city` | string | City name; surrounding spaces are removed and capitalization is normalized |
| `occupation` | string | One of `retired`, `freelancer`, `student`, `government_job`, `business_owner`, `unemployed`, or `private_job` |

The API derives BMI from weight and height, assigns an age group, calculates lifestyle risk, and determines city tier before calling the model.
