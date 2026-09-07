import matplotlib.pyplot as plt
import numpy as np

# create a simple simulated stress-strain curve (rising then falling, like real rock)
strain = np.linspace(0, 1, 200)  # 200 points from 0 to 1
stress = 4 * np.sin(strain * np.pi)  # simple curve shape: rises then falls like a rock failing

# find the peak point (where stress is highest)
peak_index = np.argmax(stress)
peak_strain = strain[peak_index]
peak_stress = stress[peak_index]

# split into pre-peak and post-peak parts
strain_before = strain[:peak_index]
stress_before = stress[:peak_index]
strain_after = strain[peak_index:]
stress_after = stress[peak_index:]

# plot the curve
plt.plot(strain, stress, color='black', linewidth=2)

# shade the pre-peak area (energy going INTO the rock)
plt.fill_between(strain_before, stress_before, color='lightblue', alpha=0.6, label='Pre-peak energy (W_E)')

# shade the post-peak area (energy needed to finish breaking it)
plt.fill_between(strain_after, stress_after, color='salmon', alpha=0.6, label='Post-peak energy (W_P)')

# mark the peak point
plt.scatter([peak_strain], [peak_stress], color='red', zorder=5, label='Peak strength')

plt.xlabel('Strain')
plt.ylabel('Stress (MPa)')
plt.title('Stress-Strain Curve: Area Under Curve = Energy')
plt.legend()
plt.show()