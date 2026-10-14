# RIDF API

Retail Inventory Demand Forecasting API built with FastAPI and XGBoost.

## Project structure

- `main.py` - FastAPI app
- `XGBR.pkl` - trained XGBoost model
- `requirements.txt` - Python dependencies

## Local setup

1. Open a terminal in the project folder.
2. Create and activate a virtual environment:

   Windows PowerShell:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   Windows Command Prompt:
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate.bat
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app locally:
   ```bash
   uvicorn main:app --reload
   ```

5. Open the API docs in your browser:
   - http://127.0.0.1:8000/docs

## API endpoint

### POST /predict

Request body example:

```json
{
  "lag_1": 3.0,
  "lag_7": 3.0,
  "rolling_mean": 0.857143,
  "day_of_week": 1,
  "month": 12
}
```

Example curl:

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"lag_1": 3.0, "lag_7": 3.0, "rolling_mean": 0.857143, "day_of_week": 1, "month": 12}'
```

## Deploy on Render

1. Push this project to GitHub.
2. Log in to Render.
3. Click New -> Web Service.
4. Connect your GitHub repository.
5. Use these settings:
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Keep `XGBR.pkl` in the project root so it is included in the deployment.
7. Deploy the service.

After deployment, Render will give you a public URL, for example:

```text
https://your-app-name.onrender.com
```

Then test:

```bash
curl https://your-app-name.onrender.com/health
```

## Troubleshooting

### `No module named uvicorn`
Use the project virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

### `ModuleNotFoundError: No module named 'xgboost'`
Install the dependency:

```bash
pip install xgboost
```

### `422 Unprocessable Entity`
Make sure your JSON request uses double quotes for all property names, such as:

```json
{
  "lag_1": 3.0,
  "lag_7": 3.0,
  "rolling_mean": 0.857143,
  "day_of_week": 1,
  "month": 12
}
```

### Model output value seems strange
If the model was trained on a transformed target, you may need to reverse the transformation before returning the result. Check the training script to confirm whether the output should be converted back using `np.expm1()` or kept as-is.

## Notes

- FastAPI auto-generates interactive docs at `/docs`.
- The app loads the model at startup, so the `.pkl` file must be present in the deployed environment.
