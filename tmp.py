import matplotlib.pyplot as plt
import numpy as np

test = ([100, 95, 85, 75, 85, 95, 100, 100, 100], [1, 2, 3, 4, 5, 6, 7, 8, 9])

fig, axs = plt.subplots()  # Create a figure containing a single Axes.
axs.plot(test[1], test[0])  # Plot some data on the Axes.
plt.show()  # Show the figure.
