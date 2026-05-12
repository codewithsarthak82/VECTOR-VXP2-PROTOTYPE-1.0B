import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure directory boundaries
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(_PROJECT_ROOT, "pitch_assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Standardize Orion Spacetech aesthetic
plt.style.use('dark_background')
sns.set_context("talk")

COLOR_PRED = '#58a6ff'       # Vector Blue
COLOR_UNCERTAINTY = '#1f6feb' # Deep Vector Blue
COLOR_TRUE = '#2ea043'       # Success Green
COLOR_ALERT = '#fa4549'      # Critical Red
COLOR_BG = '#0d1117'         # Space Black
COLOR_GRID = '#30363d'

def generate_rul_curve():
    """
    Renders high-fidelity trajectory map plotting ground truth, AI predictions, 
    and Monte Carlo Dropout uncertainty zones.
    """
    # Mock data spanning a 150-cycle engine lifespan
    cycles = np.arange(0, 150)
    true_rul = 150 - cycles
    
    # Introduce volatile aerodynamic noise resolving into the AI prediction
    np.random.seed(42)
    noise = np.random.normal(0, 3.5, size=len(cycles))
    bias = 8 * np.exp(-cycles / 40) # Overestimates early on before converging safely
    predicted_rul = true_rul + bias + noise
    
    # Uncertainty bounds simulating the MC Standard Deviation
    uncertainty = 12 - 9 * (cycles / 150) # Uncertainty restricts as data accumulates
    upper_bound = predicted_rul + uncertainty
    lower_bound = predicted_rul - uncertainty
    
    fig, ax = plt.subplots(figsize=(14, 8), facecolor=COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    
    # Extracted data render lines
    ax.plot(cycles, true_rul, color=COLOR_TRUE, linestyle='dashed', linewidth=2.5, label="Actual Ground Truth RUL")
    ax.plot(cycles, predicted_rul, color=COLOR_PRED, linewidth=3, label="Vector AI Inference Trajectory")
    
    # Confidence interval rendering
    ax.fill_between(cycles, lower_bound, upper_bound, color=COLOR_UNCERTAINTY, alpha=0.3, label="Monte Carlo Uncertainty Zone (± $\sigma$)")
    
    # Cosmetic layout and branding
    plt.title("Vector VXP2: Dynamic Flight Failure Trajectory Map", fontsize=22, fontweight='bold', color='white', pad=25)
    plt.xlabel("Engine Flight Cycles (Simulation Lifetime)", fontsize=15, color='#a1a1aa')
    plt.ylabel("Remaining Useful Engine Life (Cycles)", fontsize=15, color='#a1a1aa')
    
    plt.axhline(0, color='gray', linewidth=2, alpha=0.5)
    plt.axvline(150, color=COLOR_ALERT, linestyle='dotted', linewidth=2.5, label="Catastrophic Failure Event")
    
    # Dark Mode formatting
    legend = plt.legend(facecolor='#161b22', edgecolor='#30363d', fontsize=13, loc='upper right')
    for text in legend.get_texts():
        text.set_color("lightgray")
        
    plt.grid(color=COLOR_GRID, linestyle='-', linewidth=0.8, alpha=0.4)
    plt.text(147, 140, 'ORION SPACETECH // VXP2', color='#555555', fontsize=12, fontweight='bold', ha='right', alpha=0.6)
    
    plt.tight_layout()
    output_path = os.path.join(ASSETS_DIR, "pitch_curve_failure_prediction.png")
    
    # Render and clear pipeline
    plt.savefig(output_path, dpi=300, facecolor=ax.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"✅ Executed: Captured isolated prediction map at {output_path}")

def generate_physics_guard_comparison():
    """
    Demonstrates structural PINN override capabilities highlighting standard neural net failure.
    """
    cycles = np.arange(100, 150)
    
    # Neural Network attempts to solve shattered matrices naturally
    ai_rul = 50 - (cycles - 100) + np.random.normal(0, 1.5, size=len(cycles))
    ai_rul[30:] += np.linspace(0, 15, len(cycles[30:])) + np.random.normal(0, 5, size=len(cycles[30:]))
    
    fig, ax = plt.subplots(figsize=(14, 8), facecolor=COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    
    # 1. Healthy continuous inference zone
    ax.plot(cycles[:31], ai_rul[:31], color=COLOR_PRED, linewidth=3.5, label="Validated AI Inference")
    
    # 2. Blind Machine Learning zone (Black Box failure tracking)
    ax.plot(cycles[30:], ai_rul[30:], color='#555555', linestyle='dashed', linewidth=2.5, label="Unchecked Matrix Estimate (Standard AI)")
    
    # Physics Boundary Trigger
    violation_point = cycles[30]
    ax.axvline(violation_point, color=COLOR_ALERT, linewidth=4, linestyle='solid', label="VectorPhysicsEngine Boundary Trigger")
    
    # Paint rejection territory
    ax.fill_betweenx([0, 55], violation_point, 150, color=COLOR_ALERT, alpha=0.15)
    
    # Overlay alert text
    ax.text((int(violation_point) + 150) / 2, 28, "UNPHYSICAL STATE BLOCKED\n\n[P30 / T30 Ratio Breached]\nINFERENCE HALTED", 
            color='#ff7b72', fontweight='900', ha='center', va='center', fontsize=14, 
            bbox=dict(facecolor='#161b22', edgecolor=COLOR_ALERT, boxstyle='round,pad=1', alpha=0.9))
    
    # Presentational layouts
    plt.title("Vector VXP2: Physics-Informed Neural Override Demonstration", fontsize=22, fontweight='bold', color='white', pad=25)
    plt.xlabel("Engine Flight Cycles", fontsize=15, color='#a1a1aa')
    plt.ylabel("Inferred Operational Life (Cycles)", fontsize=15, color='#a1a1aa')
    
    plt.ylim(0, 55)
    plt.xlim(100, 150)
    
    legend = plt.legend(facecolor='#161b22', edgecolor='#30363d', fontsize=13, loc='upper right')
    for text in legend.get_texts():
        text.set_color("lightgray")
        
    plt.grid(color=COLOR_GRID, linestyle='-', linewidth=0.8, alpha=0.4)
    plt.text(148.5, 52.5, 'ORION SPACETECH // VXP2', color='#555555', fontsize=12, fontweight='bold', ha='right', alpha=0.6)
    
    plt.tight_layout()
    output_path = os.path.join(ASSETS_DIR, "pitch_pinn_guard_comparison.png")
    plt.savefig(output_path, dpi=300, facecolor=ax.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"✅ Executed: Captured physical bounds override chart at {output_path}")

if __name__ == "__main__":
    print(f"==== ENGAGING PRESENTATION ASSET GENERATOR ====\\n")
    generate_rul_curve()
    generate_physics_guard_comparison()
    print(f"\\n🚀 High-Resolution pitch graphics successfully compiled into -> {ASSETS_DIR}/")
