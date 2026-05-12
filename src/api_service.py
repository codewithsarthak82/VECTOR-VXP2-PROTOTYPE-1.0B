import os
import sys
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

# Ensure the root directory is available for module resolution
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from src.engine import VectorLSTM

# ────────────────────────────────────────────────────────────────────────────
# Application Configuration
# ────────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Vector VXP2 - Mission Control Microservice",
    description="Stand-alone predictive analytics API. Evaluates incoming stream of Flight Telemetry Data using PINN-LSTM Architecture.",
    version="2.0.0"
)

# Pre-load Core Neural Algorithms Globally
lstm_engine = VectorLSTM()
model_path = os.path.join(_PROJECT_ROOT, "models", "vxp2_lstm_v1.h5")

if os.path.exists(model_path):
    lstm_engine.model.load_weights(model_path)
    print("✅ System Core: Loaded production LSTM weights.")
else:
    print(f"⚠️ System Core: Model weights missing at {model_path}. Running localized mock-data initialization.")


# ────────────────────────────────────────────────────────────────────────────
# API Input Schemas
# ────────────────────────────────────────────────────────────────────────────
class TelemetryPacket(BaseModel):
    """
    Standardized aerospace JSON payload expecting a continuous stream of flight data.
    The Vector Engine processes standard moving windows of shape (50 Time-Steps x 21 Sensors).
    """
    sensor_sequence: List[List[float]] = Field(
        ...,
        description="A list containing 50 sub-lists. Each sub-list must contain 21 scaled sensor values corresponding to S1-S21."
    )


# ────────────────────────────────────────────────────────────────────────────
# API Endpoints
# ────────────────────────────────────────────────────────────────────────────
@app.get("/")
def health_ping():
    """Confirms Server Status to internal mission-control load balancers."""
    return {"service": "Vector VXP2 Microservice", "status": "ONLINE"}


@app.post("/predict")
def predict_telemetry(payload: TelemetryPacket):
    """
    Main Artificial Intelligence Endpoint.
    Consumes live packet matrices, executes Monte Carlo Neural Predictions, 
    evaluates mechanical thermodynamics, and outputs verified diagnostic readings.
    """
    # 1. Enforce payload flexibility via Aero-Core Padding
    try:
        sequence_tensor = np.array(payload.sensor_sequence)
        
        # Determine sequence length
        num_cycles = sequence_tensor.shape[0]
        
        if num_cycles > 50:
            # Slice to most recent window
            sequence_tensor = sequence_tensor[-50:]
        elif num_cycles < 50:
            # Apply Aero-Core Padding: Replicate the initial state
            print(f"Backend Node: Initializing Aero-Core Padding for {num_cycles} cycles.")
            padding_needed = 50 - num_cycles
            first_row = sequence_tensor[0:1, :]
            padding = np.repeat(first_row, padding_needed, axis=0)
            sequence_tensor = np.vstack([padding, sequence_tensor])
            
        # Final shape verification (Internal LSTM standard)
        if sequence_tensor.shape != (50, 21):
            raise ValueError(f"Sensor dimensionality mismatch. Expected 21 features, received {sequence_tensor.shape[1]}.")
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 2. Offload processing natively to the PINN integration (LSTM + Thermo Logic)
    try:
        report = lstm_engine.diagnose_health(sequence_tensor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal prediction engine failure: {str(e)}")

    # 3. Restructure diagnostic output JSON to the precise Microservice Schema
    pred_rul = float(report["predicted_rul"])
    sd_bound = float(report["uncertainty"])
    
    return {
        "RUL": round(pred_rul, 2),
        "Confidence_Interval": {
            "standard_deviation": round(sd_bound, 2),
            "safe_operational_lower_bound": round(pred_rul - sd_bound, 2),
            "max_expected_upper_bound": round(pred_rul + sd_bound, 2),
        },
        "Physics_Alerts": {
            "engine_status": report["physics_status"],
            "violation_flags": report["warning_flags"]
        }
    }
