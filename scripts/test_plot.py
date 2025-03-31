"""
Script for generating and saving sine wave plots
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def generate_sine_plot(output_dir="../outputs"):
    """
    Generate and save a sine wave plot
    
    Args:
        output_dir (str): Directory to save the plot (default: '../outputs')
    
    Returns:
        str: Path where the plot was saved
    """
    try:
        # Convert to Path object and create directory if needed
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate data
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        
        # Create plot
        plt.figure(figsize=(8, 4))
        plt.plot(x, y, 'b-', linewidth=2)
        plt.title("Sine Wave Plot", fontsize=14)
        plt.xlabel("X-axis", fontsize=12)
        plt.ylabel("Y-axis", fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Save plot
        plot_path = output_path / "sine_wave.png"
        plt.savefig(plot_path, dpi=100, bbox_inches='tight')
        plt.close()  # Important: close the figure to free memory
        
        print(f"Success: Plot saved to {plot_path}")
        return str(plot_path)
        
    except Exception as e:
        print(f"Error: Failed to generate plot - {str(e)}")
        return None

if __name__ == "__main__":
    generate_sine_plot()