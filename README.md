# Synthetic ADS-B Radar Simulation

This package simulates a synthetic ADS-B (Automatic Dependent Surveillance–Broadcast) environment for radar and aircraft tracking research or development. It provides tools to generate, process, and serve synthetic aircraft and radar data via HTTP APIs.

## Features

- **Synthetic ADS-B Server**: Simulates aircraft flying in a circular pattern and serves their positions in tar1090-compatible JSON format (`server.py`).
- **Bridge & Delay–Doppler Processing**: Polls the synthetic ADS-B feed, calls an external `adsb2dd` API to compute delay–Doppler measurements for three virtual radar receivers, and stores the results (`bridge.py`).
- **Radar API**: Exposes Flask-based API endpoints for each radar, providing access to computed measurements, radar status, and configuration (`radar_api.py`).
- **In-Memory Data Store**: Efficiently manages and cleans up radar measurement data (`radar_store.py`).
- **Testing**: Includes a test suite to verify server correctness and data format (`test_server.py`).

## Requirements

- Python 3.8+
- Flask 3.0.2
- Flask-CORS 4.0.0
- Requests 2.31.0

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

1. **Start the Synthetic ADS-B Server**

   ```bash
   python server.py
   ```

   This will serve synthetic aircraft data at `http://localhost:5001/data/aircraft.json`.

2. **Run the Bridge and Radar APIs**

   ```bash
   python bridge.py
   ```

   This will poll the synthetic ADS-B feed, compute delay–Doppler measurements, and start API endpoints for each radar.

3. **Access Radar Data**
   - Each radar exposes endpoints (e.g., `/data`, `/status`, `/api/detection`, `/api/config`) on its own port (default: 49158, 49159, 49160).

## Example

See `example.aircraft.json` for a sample of the synthetic ADS-B data format.

## License

MIT License
