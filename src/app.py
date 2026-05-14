"""
VECTOR VXP2 Mission Control Dashboard.
"""

import base64
import os
import sys
import time
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from src.engine import VectorInference

st.set_page_config(
    page_title="VECTOR VXP2 Mission Control",
    page_icon="V",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&display=swap');

        :root {
            --bg: #050505;
            --bg-panel: #0A0A0A;
            --bg-panel-2: #111111;
            --line: #1E1E1E;
            --line-hot: #FF0000;
            --line-warn: #D4A017;
            --text: #FFFFFF;
            --text-dim: #B5B5B5;
            --text-low: #7A7A7A;
        }

        html, body, [class*="st-"] {
            background: radial-gradient(circle at 0% 0%, #101010 0%, #050505 32%, #000000 100%);
            color: var(--text);
            font-family: 'JetBrains Mono', monospace;
        }

        /* Preserve icon glyph fonts so ligature names (e.g. keyboard_double_*) do not render as text */
        .material-icons,
        .material-symbols-outlined,
        .material-symbols-rounded,
        .material-symbols-sharp,
        [class*="material-symbols"] {
            font-family: 'Material Icons', 'Material Symbols Outlined', sans-serif !important;
            font-style: normal !important;
            letter-spacing: normal !important;
            text-transform: none !important;
            white-space: nowrap !important;
            direction: ltr !important;
        }

        .main .block-container {
            max-width: 1500px;
            padding-top: 1rem;
            padding-bottom: 1.2rem;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0A0A0A 0%, #050505 100%);
            border-right: 1px solid var(--line);
        }

        [data-testid="stSidebar"] [class*="stFileUploader"],
        [data-testid="stSidebar"] [class*="stSlider"] {
            background: #0E0E0E;
            border: 1px solid var(--line);
            border-radius: 2px;
            padding: 0.4rem 0.55rem;
        }

        /* Slider theme: solid red thumb, no blue hollow ring */
        [data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
            background: var(--line-hot) !important;
            border: 2px solid var(--line-hot) !important;
            box-shadow: none !important;
            outline: none !important;
        }
        [data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"]:focus,
        [data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"]:focus-visible {
            box-shadow: 0 0 0 2px rgba(255, 0, 0, 0.25) !important;
            outline: none !important;
        }
        [data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] div[role="progressbar"] {
            background-color: rgba(255, 0, 0, 0.22) !important;
        }
        [data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] div[role="presentation"] {
            background-color: #222222 !important;
        }

        /* Telemetry uploader cleanup: enforce a single clear upload CTA */
        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
            background: #070707;
            border: 1px dashed #333;
            border-radius: 4px;
            padding: 0 !important;
            min-height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            transition: border-color 0.3s ease;
        }

        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"]:hover {
            border-color: var(--line-hot);
        }

        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] > div:first-child {
            display: none;
        }

        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0 !important;
            background: #121212 !important;
            color: #FFFFFF !important;
            border: 1px solid #3A3A3A !important;
            border-radius: 2px !important;
            min-height: 28px !important;
            height: 28px !important;
            padding: 0 10px !important;
            position: relative !important;
            transition: all 0.2s ease;
            z-index: 2;
        }

        /* Initial state: Big clickable area within instructions */
        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            min-height: 80px !important;
        }

        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"]::after {
            content: "UPLOAD TELEMETRY" !important;
            font-family: 'Chakra Petch', sans-serif !important;
            letter-spacing: 0.1em !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            color: var(--text-dim) !important;
            position: absolute !important;
            pointer-events: none !important;
        }

        /* Force remove all default uploader internal visuals and residual boxes */
        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] > div,
        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] svg,
        [data-testid="stSidebar"] [data-testid="stFileUploaderIcon"],
        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] [class*="icon"] {
            display: none !important;
            width: 0 !important;
            height: 0 !important;
            opacity: 0 !important;
        }

        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] button {
            position: absolute !important;
            inset: 0 !important;
            width: 100% !important;
            height: 100% !important;
            background: transparent !important;
            border: none !important;
            z-index: 1;
        }

        /* Icon styling for post-upload buttons */
        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button::after {
            position: absolute !important;
            inset: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 1rem !important;
            pointer-events: none !important;
            color: #FFFFFF !important;
        }

        /* Material icons for post-upload buttons */
        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"]:nth-of-type(1):not(:only-of-type)::after {
            content: "add" !important;
            font-family: 'Material Symbols Outlined' !important;
        }
        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"]:nth-of-type(2)::after {
            content: "close" !important;
            font-family: 'Material Symbols Outlined' !important;
        }

        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button:not(:only-child) {
            width: 32px !important;
            padding: 0 !important;
            border-radius: 4px !important;
            margin-left: 4px;
        }

        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button:hover {
            border-color: var(--line-hot) !important;
            background: #1A1A1A !important;
            color: var(--line-hot) !important;
        }

        /* Hide internal labels */
        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button * {
            display: none !important;
        }

        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] small {
            color: #A8A8A8 !important;
            font-size: 0.72rem !important;
        }

        .console-section-title {
            font-family: 'Chakra Petch', sans-serif;
            color: var(--text);
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            border-bottom: 1px solid var(--line);
            padding-bottom: 0.45rem;
            margin-top: 0.8rem;
        }

        .console-card {
            background: var(--bg-panel);
            border: 1px solid var(--line);
            padding: 0.7rem;
            margin-top: 0.6rem;
        }

        .panel {
            background: linear-gradient(180deg, #0A0A0A 0%, #080808 100%);
            border: 1px solid var(--line);
            padding: 0.8rem 0.9rem;
            height: 100%;
        }

        .panel-title {
            font-family: 'Chakra Petch', sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.11em;
            color: var(--text-dim);
            font-size: 0.78rem;
            margin-bottom: 0.6rem;
        }

        .mission-header {
            background: linear-gradient(90deg, #0A0A0A 0%, #111111 60%, #0A0A0A 100%);
            border: 1px solid var(--line);
            border-top: 2px solid var(--line-hot);
            padding: 0.7rem 0.9rem;
            margin-bottom: 0.75rem;
        }

        .mission-brand {
            font-family: 'Chakra Petch', sans-serif;
            color: #FFFFFF;
            text-transform: uppercase;
            font-size: 1rem;
            letter-spacing: 0.14em;
            font-weight: 700;
        }

        .mission-sub {
            color: var(--text-dim);
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        /* Engage Simulation Button - Mission Critical Red */
        [data-testid="stSidebar"] .stButton button {
            background: #FF0000 !important;
            border: 1px solid #FF0000 !important;
            color: #FFFFFF !important;
            font-family: 'Chakra Petch', sans-serif !important;
            letter-spacing: 0.12em !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            margin-top: 1rem !important;
            border-radius: 4px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 15px rgba(255, 0, 0, 0.2) !important;
        }

        [data-testid="stSidebar"] .stButton button:hover {
            background: #CC0000 !important;
            border-color: #CC0000 !important;
            box-shadow: 0 6px 20px rgba(255, 0, 0, 0.4) !important;
            transform: translateY(-2px) !important;
        }

        [data-testid="stSidebar"] .stButton button:active {
            transform: translateY(0px) !important;
            background: #990000 !important;
        }

        .status-pill {
            display: inline-block;
            border: 1px solid var(--line);
            background: #111111;
            padding: 0.18rem 0.42rem;
            border-left: 3px solid var(--line-warn);
            font-size: 0.68rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .kpi-card {
            background: var(--bg-panel);
            border: 1px solid var(--line);
            min-height: 88px;
            padding: 0.55rem 0.7rem;
            position: relative;
        }

        .kpi-card:after {
            content: "";
            position: absolute;
            left: 0;
            bottom: 0;
            width: 100%;
            height: 2px;
            background: var(--line-hot);
            opacity: 0.65;
        }

        .kpi-label {
            color: var(--text-low);
            text-transform: uppercase;
            letter-spacing: 0.09em;
            font-size: 0.66rem;
            margin-bottom: 0.45rem;
            font-family: 'Chakra Petch', sans-serif;
        }

        .kpi-value {
            color: var(--text);
            font-size: 1.35rem;
            font-weight: 700;
        }

        .metric-small {
            color: var(--text-dim);
            font-size: 0.72rem;
            margin-top: 0.3rem;
        }

        .pipeline-strip {
            display: grid;
            grid-template-columns: repeat(5, minmax(100px, 1fr));
            gap: 0.5rem;
        }

        .pipe-item {
            border: 1px solid var(--line);
            background: #0C0C0C;
            padding: 0.45rem;
            min-height: 52px;
        }

        .pipe-name {
            color: var(--text-low);
            font-size: 0.62rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-family: 'Chakra Petch', sans-serif;
        }

        .pipe-state {
            color: var(--text);
            font-size: 0.7rem;
            margin-top: 0.3rem;
        }

        .led {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 0.35rem;
            border: 1px solid #2A2A2A;
        }

        .alert-record {
            border: 1px solid var(--line);
            background: #0C0C0C;
            padding: 0.55rem;
            margin-bottom: 0.4rem;
            font-size: 0.74rem;
            line-height: 1.4;
        }

        .alert-critical {
            background: #1A0909;
            border: 1px solid #4D1313;
            color: #FFDCDC;
        }

        .alert-warning {
            background: #171208;
            border: 1px solid #5B4718;
            color: #F3DFB5;
        }

        .alert-info {
            background: #0B0B0B;
            border: 1px solid var(--line);
            color: var(--text-dim);
        }

        .standby-msg {
            color: var(--text-low);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            border: 1px dashed #2A2A2A;
            background: #0A0A0A;
            padding: 0.6rem;
            text-align: center;
        }

        /* Floating Sidebar Toggle */
        .sidebar-toggle-container {
            position: fixed;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            z-index: 999999;
        }
        .sidebar-toggle-container button {
            background: #0A0A0A !important;
            border: 1px solid var(--line) !important;
            border-left: none !important;
            color: var(--text-dim) !important;
            padding: 1.2rem 0.4rem !important;
            border-radius: 0 4px 4px 0 !important;
            font-family: 'JetBrains Mono', monospace !important;
            transition: all 0.2s ease !important;
        }
        .sidebar-toggle-container button:hover {
            border-color: var(--line-hot) !important;
            color: var(--line-hot) !important;
            background: #111111 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_styles()

if "sidebar_collapsed" not in st.session_state:
    st.session_state.sidebar_collapsed = False

if st.session_state.sidebar_collapsed:
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            display: none !important;
        }
        .main .block-container {
            max-width: 1650px !important;
        }
        </style>
        <div class="sidebar-toggle-container">
        """,
        unsafe_allow_html=True
    )
    if st.button("keyboard_double_arrow_right", help="Expand Controls"):
        st.session_state.sidebar_collapsed = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

CMAPSS_COLS = ["unit", "cycle"] + [f"op{i}" for i in range(1, 4)] + [f"s{i}" for i in range(1, 22)]


@st.cache_resource
def load_engine() -> VectorInference | None:
    try:
        return VectorInference()
    except FileNotFoundError:
        return None


engine = load_engine()


def get_base64_image(image_path: str) -> str | None:
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def load_cmapss(file_obj) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_obj)
        if "s1" in df.columns or "s11" in df.columns:
            return df
    except Exception:
        pass
    if hasattr(file_obj, "seek"):
        file_obj.seek(0)
    df = pd.read_csv(file_obj, sep=r"\s+", header=None)
    if df.shape[1] == len(CMAPSS_COLS):
        df.columns = CMAPSS_COLS
    elif df.shape[1] == len(CMAPSS_COLS) + 2:
        df = df.iloc[:, : len(CMAPSS_COLS)]
        df.columns = CMAPSS_COLS
    else:
        df.columns = [f"col_{index}" for index in range(df.shape[1])]
    return df


def _row_to_sensor_dict(row: pd.Series) -> dict:
    row_dict = row.to_dict()
    for i in range(1, 22):
        sensor_key = f"s{i}"
        if sensor_key not in row_dict:
            row_dict[sensor_key] = 1500.0
    if "s21" in row_dict:
        row_dict["P30"] = row_dict["s21"]
    if "s9" in row_dict:
        row_dict["T30"] = row_dict["s9"]
    return row_dict


def infer_health_percent(rul: float) -> float:
    return float(max(0, min(100, (rul / 200.0) * 100)))


def infer_risk_label(rul: float, is_valid: bool) -> str:
    if rul <= 30 or not is_valid:
        return "CRITICAL"
    if rul <= 80:
        return "WARNING"
    return "INFO"


def status_color(label: str) -> str:
    if label == "CRITICAL":
        return "#FF0000"
    if label == "WARNING":
        return "#D4A017"
    if label == "LIVE":
        return "#FFFFFF"
    if label == "STANDBY":
        return "#D4A017"
    return "#7A7A7A"


def build_rul_gauge(rul_value: float) -> go.Figure:
    value = max(0, min(200, rul_value))
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": " CYC", "font": {"size": 26, "color": "#FFFFFF", "family": "JetBrains Mono"}},
            title={"text": "Remaining Useful Life", "font": {"size": 12, "color": "#B5B5B5", "family": "Chakra Petch"}},
            gauge={
                "shape": "angular",
                "axis": {"range": [0, 200], "tickcolor": "#555555", "tickwidth": 1, "tickfont": {"color": "#7A7A7A"}},
                "bar": {"color": "#FFFFFF", "thickness": 0.2},
                "bgcolor": "#090909",
                "bordercolor": "#262626",
                "borderwidth": 1,
                "steps": [
                    {"range": [0, 30], "color": "rgba(255,0,0,0.22)"},
                    {"range": [30, 80], "color": "rgba(212,160,23,0.22)"},
                    {"range": [80, 200], "color": "rgba(255,255,255,0.08)"},
                ],
                "threshold": {"line": {"color": "#FF0000", "width": 2}, "thickness": 0.8, "value": 30},
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=280,
        margin=dict(l=20, r=20, t=20, b=8),
    )
    return fig


def build_sensor_trend(cycles: list[int], values: list[float]) -> go.Figure:
    arr = np.array(values, dtype=float) if values else np.array([], dtype=float)
    marker_x = []
    marker_y = []
    if arr.size > 6:
        rolling_mean = pd.Series(arr).rolling(6, min_periods=3).mean().to_numpy()
        rolling_std = pd.Series(arr).rolling(6, min_periods=3).std().fillna(0).to_numpy()
        anomaly_idx = np.where(np.abs(arr - rolling_mean) > (1.8 * rolling_std + 1e-6))[0]
        marker_x = [cycles[i] for i in anomaly_idx]
        marker_y = [values[i] for i in anomaly_idx]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=cycles,
            y=values,
            mode="lines",
            line={"color": "#D4A017", "width": 1.6},
            name="S11",
        )
    )
    if marker_x:
        fig.add_trace(
            go.Scatter(
                x=marker_x,
                y=marker_y,
                mode="markers",
                marker={"size": 6, "color": "#FF0000", "line": {"width": 1, "color": "#370000"}},
                name="Anomaly",
            )
        )
    fig.update_layout(
        title={"text": "S11 - TURBINE OUTLET TEMPERATURE", "font": {"size": 12, "family": "Chakra Petch", "color": "#B5B5B5"}},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#090909",
        margin=dict(l=45, r=20, t=38, b=30),
        showlegend=False,
        xaxis={"title": "Cycle", "gridcolor": "rgba(255,255,255,0.06)", "color": "#7A7A7A"},
        yaxis={"title": "Temperature", "gridcolor": "rgba(255,255,255,0.06)", "color": "#7A7A7A"},
        height=400,
    )
    return fig


def MissionHeader(status: str) -> None:
    logo_path = os.path.join(_PROJECT_ROOT, "media", "Logo-1 PNG.png")
    logo_html = "ORION SPACETECH"
    logo_b64 = get_base64_image(logo_path)
    if logo_b64:
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height:34px;" alt="ORION SPACETECH">'
    now_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session_id = f"SESSION-{datetime.now().strftime('%H%M%S')}"
    left, right = st.columns([3, 2])
    with left:
        st.markdown(
            f"""
            <div class="mission-header">
                <div style="display:flex; justify-content:space-between; align-items:center; gap:0.6rem;">
                    <div>
                        <div>{logo_html}</div>
                        <div class="mission-brand">VECTOR VXP2</div>
                        <div class="mission-sub">VECTOR VXP2 Predictive Maintenance Intelligence</div>
                    </div>
                    <div class="status-pill" style="border-left-color:{status_color(status)}; color:{status_color(status)};">
                        {status}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            f"""
            <div class="mission-header">
                <div style="display:flex; justify-content:space-between; font-size:0.73rem; color:#B5B5B5;">
                    <span>Deploy</span>
                    <span>Settings</span>
                </div>
                <div style="margin-top:0.6rem; color:#7A7A7A; font-size:0.7rem;">{now_stamp}</div>
                <div style="color:#7A7A7A; font-size:0.7rem;">{session_id}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def TelemetrySidebar(uploaded_file, sim_speed, buffer_size, noise_level) -> None:
    if uploaded_file is None:
        status_text = "STANDBY: Awaiting telemetry stream"
        status_color_value = "#D4A017"
        file_name = "No file loaded"
        file_size = "-"
    else:
        status_text = "Validation complete"
        status_color_value = "#FFFFFF"
        file_name = uploaded_file.name
        file_size = f"{uploaded_file.size / 1024:.1f} KB"
    st.markdown('<div class="console-section-title">TELEMETRY STREAM</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="console-card">
            <div style="font-size:0.7rem;color:#7A7A7A;">File</div>
            <div style="font-size:0.78rem;color:#FFFFFF; margin-bottom:0.3rem;">{file_name}</div>
            <div style="font-size:0.7rem;color:#7A7A7A;">Size</div>
            <div style="font-size:0.75rem;color:#B5B5B5; margin-bottom:0.3rem;">{file_size}</div>
            <div style="font-size:0.7rem;color:#7A7A7A;">Status</div>
            <div style="font-size:0.75rem;color:{status_color_value};">{status_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="console-section-title">Simulation Controls</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="console-card">
            <div style="font-size:0.72rem;color:#B5B5B5; line-height:1.6;">
                Playback speed: <span style="color:#FFFFFF;">{sim_speed:.2f} sec/cycle</span><br>
                Buffer size: <span style="color:#FFFFFF;">{buffer_size}</span><br>
                Noise level: <span style="color:#FFFFFF;">{noise_level}%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def StatusKPICard(label: str, value: str, subtext: str = "", hot_line: str = "#FF0000") -> None:
    st.markdown(
        f"""
        <div class="kpi-card" style="--line-hot:{hot_line};">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="metric-small">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def AlertCenter(alert_rows: list[dict]) -> None:
    st.markdown('<div class="panel-title">ALERT CENTER</div>', unsafe_allow_html=True)
    if not alert_rows:
        st.markdown('<div class="standby-msg">STANDBY: Awaiting telemetry stream</div>', unsafe_allow_html=True)
        return
    for alert in alert_rows[-4:][::-1]:
        severity = alert["severity"]
        css_class = "alert-info"
        if severity == "WARNING":
            css_class = "alert-warning"
        if severity == "CRITICAL":
            css_class = "alert-critical"
        st.markdown(
            f"""
            <div class="alert-record {css_class}">
                <strong>{severity}</strong> | CYCLE {alert['cycle']} | PARAMETER {alert['parameter']}<br>
                Predicted Impact: {alert['impact']}<br>
                Recommended Action: {alert['action']}
            </div>
            """,
            unsafe_allow_html=True,
        )


def RULGauge(current_rul: float) -> None:
    st.plotly_chart(build_rul_gauge(current_rul), use_container_width=True)


def SensorTrendChart(cycles: list[int], s11_values: list[float]) -> None:
    st.plotly_chart(build_sensor_trend(cycles, s11_values), use_container_width=True)


def EngineHealthPanel(status: str, confidence: float, current_cycle: int, health_percent: float, rul_value: float) -> None:
    st.markdown('<div class="panel-title">Engine Health Console</div>', unsafe_allow_html=True)
    left, right = st.columns([1.2, 1])
    with left:
        RULGauge(rul_value)
    with right:
        st.markdown(
            f"""
            <div class="console-card" style="min-height:282px;">
                <div style="color:#7A7A7A;font-size:0.68rem;">Health Status</div>
                <div style="color:{status_color(status)};font-size:1.1rem; margin-bottom:0.6rem;">{status}</div>
                <div style="color:#7A7A7A;font-size:0.68rem;">Anomaly Confidence</div>
                <div style="color:#FFFFFF;font-size:1.02rem; margin-bottom:0.6rem;">{confidence:.1f}%</div>
                <div style="color:#7A7A7A;font-size:0.68rem;">Current Cycle</div>
                <div style="color:#FFFFFF;font-size:1.02rem; margin-bottom:0.6rem;">{current_cycle}</div>
                <div style="color:#7A7A7A;font-size:0.68rem;">Sensor Deviation</div>
                <div style="color:#B5B5B5;font-size:0.92rem; margin-bottom:0.6rem;">{100 - health_percent:.1f}%</div>
                <div style="color:#7A7A7A;font-size:0.68rem;">Recommended Maintenance Window</div>
                <div style="color:#D4A017;font-size:0.92rem;">{max(0, int(rul_value - 20))} to {max(0, int(rul_value))} cycles</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


with st.sidebar:
    st.markdown('<div class="console-section-title">Telemetry Input + Simulation Controls</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Telemetry Stream", type=["csv", "txt"], label_visibility="collapsed")
    sim_speed = st.slider("Playback speed", 0.03, 0.60, 0.12, 0.01)
    buffer_size = st.slider("Buffer size", 20, 220, 60, 10)
    noise_level = st.slider("Noise level (%)", 0, 15, 0, 1)
    def on_engage():
        st.session_state.sidebar_collapsed = True

    auto_run = st.button("ENGAGE SIMULATION", on_click=on_engage, use_container_width=True)
    TelemetrySidebar(uploaded_file, sim_speed, buffer_size, noise_level)


status_state = "OFFLINE"
if uploaded_file is not None:
    status_state = "STANDBY"
if auto_run:
    status_state = "LIVE"
MissionHeader(status_state)

if uploaded_file is None:
    st.markdown('<div class="standby-msg">STANDBY: Awaiting telemetry stream</div>', unsafe_allow_html=True)
    st.stop()

df = load_cmapss(uploaded_file)
units = sorted(df["unit"].unique()) if "unit" in df.columns else [1]
with st.sidebar:
    selected_unit = st.selectbox("Engine Unit", units)
unit_df = df[df["unit"] == selected_unit].reset_index(drop=True) if "unit" in df.columns else df.copy()

total_cycles = int(unit_df["cycle"].max()) if "cycle" in unit_df.columns else len(unit_df)
sensor_count = len([column for column in unit_df.columns if str(column).startswith("s")])

last_rul = float(total_cycles)
last_valid = True
last_cycle = 0
s11_hist: list[float] = []
cycles_hist: list[int] = []
alerts: list[dict] = []

if auto_run and engine is None:
    st.error("Model missing at `models/rf_v1.pkl`. Training artifact required for simulation.")
    st.stop()

if auto_run:
    for idx in range(len(unit_df)):
        row = unit_df.iloc[idx].copy()
        if noise_level > 0:
            noise_factor = noise_level / 100.0
            for column in row.index:
                if str(column).startswith("s") or column in ["op1", "op2", "op3", "P30", "T30"]:
                    try:
                        row[column] = float(row[column]) * (1.0 + np.random.normal(0, noise_factor))
                    except (TypeError, ValueError):
                        continue
        row_dict = _row_to_sensor_dict(row)
        rul = engine.predict_rul(row_dict)
        is_valid, guard_msg = engine.physics_guardrail(row_dict)
        cycle_num = int(row.get("cycle", idx + 1))
        s11_value = float(row.get("s11", 0.0))

        last_rul = float(rul)
        last_valid = bool(is_valid)
        last_cycle = cycle_num
        cycles_hist.append(cycle_num)
        s11_hist.append(s11_value)

        severity = infer_risk_label(last_rul, last_valid)
        impact = "RUL decline likely within short horizon" if severity != "INFO" else "Nominal trend maintained"
        action = "Inspect compressor thermal profile and schedule controlled shutdown" if severity == "CRITICAL" else (
            "Increase telemetry sampling and monitor drift" if severity == "WARNING" else "Continue nominal monitoring"
        )
        alerts.append(
            {
                "severity": severity,
                "cycle": cycle_num,
                "parameter": "S11 / P30-T30",
                "impact": impact,
                "action": action,
                "message": guard_msg,
            }
        )
        time.sleep(sim_speed)

health_percent = infer_health_percent(last_rul)
risk_level = infer_risk_label(last_rul, last_valid)
confidence = 95.0 if last_valid else 61.0

kpi_cols = st.columns(6)
with kpi_cols[0]:
    StatusKPICard("Engine Unit", f"#{selected_unit}", "Telemetry target", "#FF0000")
with kpi_cols[1]:
    StatusKPICard("Total Cycles", str(total_cycles), "Loaded sequence", "#D4A017")
with kpi_cols[2]:
    StatusKPICard("Sensors Active", str(sensor_count), "Sensor bus", "#D4A017")
with kpi_cols[3]:
    StatusKPICard("Engine Health %", f"{health_percent:.1f}", "Composite score", "#FF0000")
with kpi_cols[4]:
    StatusKPICard("RUL", f"{last_rul:.1f}", "Cycles", "#FF0000")
with kpi_cols[5]:
    StatusKPICard("Risk Level", risk_level, "Assessment", "#D4A017" if risk_level == "WARNING" else "#FF0000")

st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
st.markdown('<div class="panel">', unsafe_allow_html=True)
EngineHealthPanel(risk_level if auto_run else "STANDBY", confidence, last_cycle, health_percent, last_rul)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
st.markdown('<div class="panel"><div class="panel-title">Sensor Trend Panel</div>', unsafe_allow_html=True)
if auto_run:
    SensorTrendChart(cycles_hist[-buffer_size:], s11_hist[-buffer_size:])
else:
    st.markdown('<div class="standby-msg">LIVE TELEMETRY ACTIVE after simulation engage</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
st.markdown('<div class="panel">', unsafe_allow_html=True)
AlertCenter(alerts if auto_run else [])
st.markdown('</div>', unsafe_allow_html=True)
