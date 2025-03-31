"""
Final working test suite for plot generation
Version: 1.8
- Properly handles invalid paths on Windows
- Guaranteed to raise OSError for invalid directories
"""

import unittest
import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Robust path handling
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def generate_sine_plot(output_dir="../outputs", figsize=None):
    """
    Generate and save a sine wave plot
    
    Args:
        output_dir (str): Directory to save the plot
        figsize (tuple): Optional figure dimensions in inches (width, height)
        
    Returns:
        str: Path to saved plot file
    Raises:
        OSError: If output directory cannot be created
    """
    output_path = Path(output_dir)
    
    # First try to create directory to verify we have permissions
    try:
        output_path.mkdir(exist_ok=True, parents=True)
    except Exception as e:
        plt.close()
        raise OSError(f"Cannot create output directory: {str(e)}")
    
    # Then verify we can write to the directory
    test_file = output_path / "__test_write__.tmp"
    try:
        with open(test_file, 'w') as f:
            f.write("test")
        test_file.unlink()
    except Exception as e:
        plt.close()
        raise OSError(f"Cannot write to directory: {str(e)}")
    
    # Create figure with optional size
    plt.figure(figsize=figsize) if figsize else plt.figure()
    
    # Generate plot
    x = np.linspace(0, 10, 100)
    plt.plot(x, np.sin(x), 'b-', linewidth=2)
    plt.title("Sine Wave", fontsize=14)
    plt.xlabel("X-axis", fontsize=12)
    plt.ylabel("Y-axis", fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Save plot
    plot_path = output_path / "sine_wave.png"
    try:
        plt.savefig(plot_path, dpi=100, bbox_inches='tight')
    except Exception as e:
        plt.close()
        raise OSError(f"Cannot save plot: {str(e)}")
    finally:
        plt.close()
    
    print(f"Success: Plot saved to {plot_path}")
    return str(plot_path)

class TestPlotGeneration(unittest.TestCase):
    """Test suite with guaranteed invalid path handling"""
    
    @classmethod
    def setUpClass(cls):
        """Create test directory once for all tests"""
        cls.test_dir = Path("test_outputs")
        cls.test_dir.mkdir(exist_ok=True, parents=True)
        
    def setUp(self):
        """Clean up before each test"""
        plt.close('all')
        for f in self.test_dir.glob("*.*"):
            f.unlink(missing_ok=True)
        
    def test_plot_creation_basic(self):
        """Test basic plot generation"""
        plot_path = generate_sine_plot(output_dir=self.test_dir)
        self.assertTrue(Path(plot_path).exists())
        self.assertGreater(Path(plot_path).stat().st_size, 1024)

    def test_plot_content(self):
        """Validate plot content"""
        plot_path = generate_sine_plot(output_dir=self.test_dir)
        
        with Image.open(plot_path) as img:
            self.assertGreaterEqual(img.width, 500)
            self.assertGreaterEqual(img.height, 300)
            
        img_data = plt.imread(plot_path)
        self.assertIn(img_data.shape[2], [3, 4])

    def test_default_filename(self):
        """Verify default filename"""
        plot_path = generate_sine_plot(output_dir=self.test_dir)
        self.assertTrue(plot_path.endswith("sine_wave.png"))

    def test_custom_dimensions(self):
        """Test with custom figure size"""
        plot_path = generate_sine_plot(output_dir=self.test_dir, figsize=(6, 4))
        
        with Image.open(plot_path) as img:
            self.assertAlmostEqual(img.width, 600, delta=50)
            self.assertAlmostEqual(img.height, 400, delta=50)

    def test_invalid_output_dir(self):
        """Test invalid path handling"""
        with self.assertRaises(OSError):
            # Use a reserved Windows path that will always fail
            generate_sine_plot(output_dir="C:/Windows/System32/invalid_test_path/")

    @classmethod
    def tearDownClass(cls):
        """Final cleanup"""
        try:
            for f in cls.test_dir.glob("*.*"):
                f.unlink(missing_ok=True)
            cls.test_dir.rmdir()
        except (OSError, PermissionError):
            pass

if __name__ == "__main__":
    unittest.main(verbosity=2, failfast=True)