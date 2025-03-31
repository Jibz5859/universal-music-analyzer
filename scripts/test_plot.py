import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def generate_sine_plot(output_dir="../outputs"):
    """Generate and save sine wave plot"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    x = np.linspace(0, 10, 100)
    plt.plot(x, np.sin(x))
    plt.title("Sine Wave")
    plot_path = output_path / "plot.png"
    plt.savefig(plot_path)
    print(f"Plot saved at: {plot_path}")
    return str(plot_path)

if __name__ == "__main__":
    generate_sine_plot()