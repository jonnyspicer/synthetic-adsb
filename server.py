#!/usr/bin/env python3
"""
synthetic_adsb_server.py

A Flask-based HTTP server that serves synthetic ADS-B data in tar1090 format.
Simulates one aircraft flying in a circular pattern around Mount Lofty (–34.9810, 138.7081),
at a constant barometric altitude, updating once per second.

Endpoint:
  GET /data/aircraft.json

Response schema:
{
  "now": <epoch seconds float>,
  "aircraft": [
    {
      "hex": <string>,         # ICAO hex address
      "lat": <float>,          # degrees
      "lon": <float>,          # degrees
      "alt_baro": <int>,       # feet
      "alt_geom": <int>,        # feet
      "flight": <string>,      # Synthetic flight number with padding
      "seen_pos": 0
    },
    … (more aircraft)
  ]
}
"""

import time
import math
import threading
from flask import Flask, jsonify
from flask_cors import CORS

# -------------------------------------------------------------------
# Configuration: transmitter atop Mount Lofty
# -------------------------------------------------------------------
TX_LAT   = -34.9810   # degrees
TX_LON   = 138.7081   # degrees
TX_ALT   = 750        # meters AMSL (not used by this server)
FC_MHZ   = 204.64     # MHz DVB-T (for downstream adsb2dd)

# Synthetic flight parameters
RADIUS_DEG     = 0.05      # ~5.5 km circle radius
ANGULAR_SPEED = 0.01       # radians per second (full circle ~10 minutes)
ALT_BARO_FT   = 30000      # constant barometric altitude in feet
ICAO_HEX      = "AEF123"   # fixed hex code for synthetic aircraft

# Server settings
HOST = "0.0.0.0"
PORT = 5001

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/data/aircraft.json")
def serve_synthetic_adsb():
    """
    Generate one circular-flight aircraft at the current time.
    """
    now = time.time()
    theta = (now * ANGULAR_SPEED) % (2 * math.pi)

    # Compute position around Mount Lofty
    lat = TX_LAT + RADIUS_DEG * math.cos(theta)
    lon = TX_LON + RADIUS_DEG * math.sin(theta)

    aircraft = {
        "hex": ICAO_HEX,
        "lat": round(lat, 6),
        "lon": round(lon, 6),
        "alt_baro": ALT_BARO_FT,
        "alt_geom": ALT_BARO_FT + 100,  # Geometric altitude is typically slightly higher
        "flight": "SYN001  ",  # Synthetic flight number with padding
        "seen_pos": 0
    }

    return jsonify({
        "now": now,
        "aircraft": [aircraft]
    })

def run_server():
    app.run(host=HOST, port=PORT, threaded=True)

if __name__ == "__main__":
    print(f"[synthetic_adsb_server] starting on http://{HOST}:{PORT}/data/aircraft.json")
    threading.Thread(target=run_server, daemon=True).start()

    try:
        # Keep the main thread alive
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("\n[synthetic_adsb_server] shutting down.")
