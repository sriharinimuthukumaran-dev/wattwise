# WattWise

AI-Driven Home Energy Management and Appliance-Level Optimization.

WattWise is a smart home energy optimization platform that helps homeowners monitor consumption, forecast demand, and schedule high-load appliances to reduce electricity costs, smooth peak demand, and improve comfort.

## Features

- Real-time home energy monitoring dashboard
- Appliance-level load profiling
- 24-hour and 7-day demand forecasting
- AI-assisted optimization recommendations
- Peak-shaving and time-of-use cost reduction
- Smart home scheduling for flexible appliances
- JSON API for integration with other systems

## Tech stack

- FastAPI backend
- Vanilla JavaScript frontend
- Python-based optimization engine
- Forecasting and scheduling heuristics

## Project structure

- `app/` - backend application and optimization logic
- `static/` - frontend assets
- `requirements.txt` - Python dependencies

## Quick start

1. Create and activate a virtual environment
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
4. Open the dashboard at `http://localhost:8000/`

## API endpoints

- `GET /api/health`
- `GET /api/overview`
- `GET /api/forecast`
- `GET /api/appliances`
- `GET /api/optimization`

## Example usage

```bash
curl http://localhost:8000/api/overview
curl http://localhost:8000/api/optimization
```

## License

MIT
