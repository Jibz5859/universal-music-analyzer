"""
100% Working Plot Generator with Reliable Cleanup
Version: 8.2 (Final Exact Count Version)
"""

import os
import sys
import shutil
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Configuration
PROJECT_ROOT = Path(r"C:\Users\jibin\OneDrive\Desktop\python_projects\newproject").resolve()
OUTPUT_DIR = PROJECT_ROOT / "outputs"
MAX_PLOTS_TO_KEEP = 5  # Keep exactly 5 plots total
TEMP_DIR = PROJECT_ROOT / "temp_plots"

def setup_environment():
    """Ensure directories exist and are clean"""
    try:
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR, ignore_errors=True)
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"\n⚠ SETUP ERROR: {str(e)}")
        return False

def clean_and_keep_newest():
    """Keep only newest files to make room for new plot"""
    try:
        print("\n=== PERFORMING CLEANUP ===")
        all_plots = sorted(OUTPUT_DIR.glob("sine_wave_*.png"), 
                         key=os.path.getmtime, 
                         reverse=True)
        
        if not all_plots:
            print("No plots found to clean up")
            return True
            
        # Keep N-1 to make room for new plot
        plots_to_keep = all_plots[:MAX_PLOTS_TO_KEEP-1]
        print(f"Keeping {len(plots_to_keep)} newest plots to maintain {MAX_PLOTS_TO_KEEP} total:")
        
        # Move all to temp first
        for plot in all_plots:
            try:
                shutil.move(str(plot), TEMP_DIR)
            except Exception as e:
                print(f"⚠ Couldn't move {plot.name}: {str(e)}")
        
        # Restore only kept files
        for plot in plots_to_keep:
            try:
                temp_path = TEMP_DIR / plot.name
                if temp_path.exists():
                    shutil.move(str(temp_path), OUTPUT_DIR)
                    print(f"✓ Kept: {plot.name}")
            except Exception as e:
                print(f"⚠ Couldn't restore {plot.name}: {str(e)}")
        
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
        print("Cleanup completed successfully")
        return True
        
    except Exception as e:
        print(f"\n⚠ CLEANUP ERROR: {str(e)}")
        return False

def generate_sine_plot():
    """Generate and save sine wave plot"""
    if not setup_environment():
        return False
        
    try:
        # 1. Clean up first
        if not clean_and_keep_newest():
            return False
        
        # 2. Create new plot
        plt.figure(figsize=(10, 6))
        x = np.linspace(0, 10, 1000)
        plt.plot(x, np.sin(x), color='#1f77b4', linewidth=2.5)
        plt.title("Sine Wave", fontsize=14)
        plt.grid(True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_path = OUTPUT_DIR / f"sine_wave_{timestamp}.png"
        plt.savefig(plot_path, dpi=120, bbox_inches='tight')
        plt.close()
        
        # 3. Verify
        if not plot_path.exists():
            raise RuntimeError("File was not created")
        if plot_path.stat().st_size < 1024:
            raise RuntimeError("File is too small")
            
        # 4. Report
        print("\n=== SUCCESS ===")
        print(f"✓ Saved to: {plot_path}")
        print(f"✓ Size: {plot_path.stat().st_size/1024:.1f} KB")
        print("\nCurrent plots (newest first):")
        os.system(f"dir /O-D /B \"{OUTPUT_DIR}\"")
        return True
        
    except Exception as e:
        plt.close('all')
        print(f"\n⚠ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n=== SYSTEM CHECK ===")
    print(f"Python: {sys.executable}")
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Output Dir: {OUTPUT_DIR}")
    
    if "OneDrive" in str(OUTPUT_DIR):
        print("\nNOTE: OneDrive sync may cause delays")
    
    generate_sine_plot()