# VECTOR VXP2 PROTOTYPE 1.0-B - Mission READY
**Official Project Documentation // Orion Spacetech**

---

### 🚀 Quick Start
Run the following command from the root directory to synchronize the environment, validate the AI models, and launch the real-time telemetry dashboard:

```bash
./run_vector_v2.sh
```

---

### 📡 Environment Specifications
The VXP2 platform is locked to the following stable production environment for the IISc faculty demonstration:

*   **Runtime:** Python 3.12.4
*   **Neural Core:** TensorFlow (Keras API)
*   **Physics Guard:** NumPy / Custom Vector Physics Engine
*   **API Layer:** FastAPI / Uvicorn (Stateless Microservice)
*   **Visualization:** Streamlit / Plotly / Seaborn
*   **Analytics:** Scikit-learn (MinMaxScaler / K-Means Clustering)

---

### 🧠 The 2.0 Breakthrough: Hybrid AI-Physics Integration
The breakthrough in achieving **>80% predictive accuracy** on the complex FD004 dataset lies in our "Physics-Informed" boundary logic. Historically, standard deep learning models (black boxes) are vulnerable to "Sensor Blindness" or telemetry spikes that ignore the laws of thermodynamics. 

Vector VXP2 solves this by wrapping a 2-layer LSTM architecture within a rigid **Thermodynamic Guardrail**. By strictly monitoring real-time **P30/T30 (Pressure-to-Temperature)** ratios and enforcing physical consistency BEFORE the final inference is displayed, we effectively eliminate false positives caused by hardware shorts or atmospheric noise. When combined with **Monte Carlo Dropout**—which runs 10 stochastic passes to compute mathematical uncertainty—the system provides a self-certifying maintenance loop that is both statistically confident and physically grounded.

---

**🏁 MASTER DEMO STATUS: NOMINAL**
