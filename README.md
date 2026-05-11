# VXP2-IISC-PROTOTYPE
This repository contains our VXP2 Iteration 1.0B for IISc FSID/STEM Technical Assessment. Hybrid AI-Physics Predictive Maintenance for Aerospace. Integrating LSTM Neural Networks with Thermodynamic Guardrails to achieve >80% accuracy in engine RUL prediction. Built for Orion Spacetech.

# VECTOR VXP2 Prototype 1.0B -
**Physics-Informed Neural Networks (PINN) for Next-Gen Aerospace Reliability**

VECTOR VXP2 is a predictive maintenance platform designed by **Orion Spacetech** to solve the aerospace certification bottleneck. It transitions predictive analytics from simple "black-box" AI to a self-certifying, physics-grounded architecture.

### Core Innovations
*   **Hybrid AI-Physics Integration:** A 2-layer LSTM architecture wrapped in a **Thermodynamic Guardrail**. The system validates real-time P30/T30 ratios before inference to eliminate false positives caused by sensor noise.
*   **Mathematical Uncertainty:** Implements **Monte Carlo Dropout** to provide a statistical confidence interval (Standard Deviation) for Remaining Useful Life (RUL) predictions.
*   **Real-time Telemetry:** A Streamlit-based command center for live engine health monitoring and diagnostic alerts.
*   **Dataset:** Trained and validated on the complex **NASA CMAPSS FD004** turbofan dataset.

### Tech Stack
*   **Neural Core:** TensorFlow / Keras (LSTM)
*   **Physics Engine:** NumPy / Custom Vector Physics Logic
*   **Dashboard:** Streamlit / Plotly
*   **Runtime:** Python 3.12+

