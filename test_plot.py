import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Create sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)
df = pd.DataFrame({'x': x, 'y': y})

# Plot
df.plot('x', 'y', title='Sine Wave')
plt.savefig('plot.png')
print("Plot saved as plot.png")