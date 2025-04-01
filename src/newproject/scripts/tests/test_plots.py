"""
Production-Grade Plot Generator with Auto-Cleanup
Version: 8.3 (Final Release)
"""

import os
import sys
import shutil
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Configuration - Safe to Modify
PROJECT_ROOT = Path(r"C:\Users\jibin\OneDrive\Desktop\python_projects\newproject").resolve()
OUTPUT_DIR = PROJECT_ROOT / "outputs"
MAX_PLOTS_TO_KEEP = 5  # Maintain exactly 5 plots
TEMP_DIR = PROJECT_ROOT / "_cleanup_temp"  # Hidden temp folder

def setup_environment():
    """Initialize directories with enhanced error handling"""
    try:
        # Use hidden temp folder to avoid OneDrive sync
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR, ignore_errors=True)
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        
        # Ensure output directory exists
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        return True
        
    except Exception as e:
        print(f"\n🛑 SETUP FAILED: {str(e)}")
        return False

def maintain_plot_count():
    """Keep only newest files to maintain exact count"""
    try:
        print("\n🔧 Performing cleanup...")
        all_plots = sorted(OUTPUT_DIR.glob("sine_wave_*.png"), 
                         key=os.path.getmtime, 
                         reverse=True)
        
        if len(all_plots) <= MAX_PLOTS_TO_KEEP - 1:
            print(f"✔ No cleanup needed ({len(all_plots)} files)")
            return True
            
        # Calculate how many to keep (making room for new plot)
        keep_count = MAX_PLOTS_TO_KEEP - 1
        print(f"Keeping {keep_count} newest of {len(all_plots)} existing plots")
        
        # Move all to temp first (safer than direct delete)
        for plot in all_plots:
            try:
                shutil.move(str(plot), TEMP_DIR)
            except Exception as e:
                print(f"⚠ Couldn't move {plot.name}: {str(e)}")
        
        # Restore only the files we want to keep
        kept_files = 0
        for plot in all_plots[:keep_count]:
            try:
                temp_path = TEMP_DIR / plot.name
                if temp_path.exists():
                    shutil.move(str(temp_path), OUTPUT_DIR)
                    kept_files += 1
                    print(f"✔ Kept: {plot.name}")
            except Exception as e:
                print(f"🛑 Failed to restore {plot.name}: {str(e)}")
        
        # Final cleanup
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
        print(f"✔ Cleanup complete ({kept_files} files retained)")
        return True
        
    except Exception as e:
        print(f"\n🛑 CLEANUP FAILED: {str(e)}")
        return False

def generate_plot():
    """Generate and save a new sine wave plot"""
    try:
        # Setup and cleanup
        if not setup_environment() or not maintain_plot_count():
            return False
        
        # Create high-quality plot
        plt.figure(figsize=(10, 6), dpi=120)
        x = np.linspace(0, 10, 1000)
        plt.plot(x, np.sin(x), color='#1f77b4', linewidth=2.5, alpha=0.8)
        plt.title("Sine Wave", fontsize=14, pad=10)
        plt.xlabel("X-axis", fontsize=12)
        plt.ylabel("Y-axis", fontsize=12)
        plt.grid(True, linestyle=':', alpha=0.5)
        
        # Save with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_path = OUTPUT_DIR / f"sine_wave_{timestamp}.png"
        plt.savefig(plot_path, bbox_inches='tight', facecolor='white')
        plt.close()
        
        # Verify output
        if not plot_path.exists():
            raise RuntimeError("File not created")
        if plot_path.stat().st_size < 1024:
            raise RuntimeError("File too small")
            
        # Success report
        print("\n🎉 PLOT GENERATED SUCCESSFULLY")
        print(f"📍 Location: {plot_path}")
        print(f"📏 Size: {plot_path.stat().st_size/1024:.1f} KB")
        print("\n📂 Current plots (newest first):")
        os.system(f"dir /O-D /B \"{OUTPUT_DIR}\"")
        return True
        
    except Exception as e:
        plt.close('all')
        print(f"\n🛑 GENERATION FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n" + "="*40)
    print("SYSTEM CHECK".center(40))
    print("="*40)
    print(f"🐍 Python: {sys.executable}")
    print(f"📁 Project: {PROJECT_ROOT}")
    print(f"💾 Output: {OUTPUT_DIR}")
    print(f"🔒 Writable: {os.access(OUTPUT_DIR, os.W_OK)}")
    
    if "OneDrive" in str(OUTPUT_DIR):
        print("\nℹ NOTE: OneDrive sync may cause brief delays")
    
    print("\n" + "="*40)
    print("GENERATING PLOT".center(40))
    print("="*40)
    
    if not generate_plot():
        sys.exit(1)