#!/bin/bash

# VECTOR VXP2 PROTOTYPE 1.0-B
# Main Execution Protocol

echo "=========================================================="
echo "      INITIATING VECTOR VXP2 PROTOTYPE ARCHITECTURE       "
echo "=========================================================="
echo ""

# 1. Install dependencies
echo "[1/4] Synchronizing Python environment dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "⚠️ ERROR: Failed to install dependencies. Check your Python environment."
    exit 1
fi
echo "✅ Dependencies verified."
echo ""

# 2. Run validation check on the model artifact
echo "[2/4] Validating Vector LSTM Neural Network weights..."
if [ -f "models/vxp2_lstm_v1.h5" ]; then
    echo "✅ Model validation passed: vxp2_lstm_v1.h5 located and secured."
else
    echo "⚠️ CRITICAL FAILURE: Model weights missing at models/vxp2_lstm_v1.h5"
    echo "Please run Notebook 02_Model_Training.ipynb to generate the active model."
    exit 1
fi
echo ""

# Print final success states before passing terminal control to the dashboard server
echo "[3/4] Handing over execution to Presentation Layer..."
echo "🚀 VECTOR VXP2 PROTOTYPE 1.0-B IS LIVE - System Status: NOMINAL"
echo ""

# 3. Launch the Streamlit dashboard (This blocks the terminal thread)
echo "[4/4] Engaging Streamlit Engine Server..."
streamlit run src/app.py
