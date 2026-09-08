# Rockburst Proneness Criteria Calculator
# Based on Wibisono, Arora & Gutierrez (2022), ARMA 22-2032
# ---------- Step 1: A four-criteria calculator ----------
# ---------- Criterion 1: Strength Brittleness Index (B1) ----------
def calculate_b1(sigma_c, sigma_t):
    """B1 = compressive strength / tensile strength"""
    return sigma_c / sigma_t

def classify_b1(b1):
    if b1 > 40:
        return "no rockburst"
    elif b1 > 26.7:
        return "weak rockburst"
    elif b1 > 14.5:
        return "medium rockburst"
    else:
        return "strong rockburst"


# ---------- Criterion 2: Burst Energy Coefficient (R) ----------
def calculate_r(w_e, w_p):
    """R = pre-peak energy / post-peak energy"""
    return w_e / w_p

def classify_r(r):
    if r > 1:
        return "bursting rock"
    else:
        return "non-bursting rock"


# ---------- Criterion 3: Brittleness Index Modified (BIM) ----------
def calculate_bim(a2, a1):
    """BIM = total pre-peak energy / peak elastic strain energy"""
    return a2 / a1

def classify_bim(bim): 
    """thresholds approximated from Fig. 7, not exact — verify with Prof. Adoko 
    if this criterion is used for real analysis"""
    if bim <= 1.1:
        return "high bursting liability"
    elif bim <= 1.3:
        return "moderate-to-high bursting liability"
    else:
        return "low bursting liability"


# ---------- Criterion 4: Strain Energy Storage Index (F) ----------
def calculate_f(phi_sp, phi_st):
    """F = retained elastic energy / dissipated energy"""
    return phi_sp / phi_st

def classify_f(f):
    if f > 5.0:
        return "strong-to-violent shock"
    elif f > 2.0:
        return "weak-to-medium shock"
    else:
        return "no shock"


# ---------- Test with the paper's actual reported values ----------
print("=== Testing against ARMA paper's reported values ===\n")

# B1: paper reports sigma_c = 3.07 MPa, sigma_t = 0.45 MPa
b1 = calculate_b1(3.07, 0.45)
print(f"B1 = {b1:.2f} -> {classify_b1(b1)}")
print(f"(Paper reported B1 range: 5.1-9.6, classified as strong rockburst)\n")

# R: paper reports W_E = 6.5e-3, W_P = 5e-3
r = calculate_r(6.5e-3, 5e-3)
print(f"R = {r:.2f} -> {classify_r(r)}")
print(f"(Paper reported R = 1.3, classified as bursting rock)\n")

# BIM: paper reports A2 = 6.5e-3, A1 = 5.5e-3
bim = calculate_bim(6.5e-3, 5.5e-3)
print(f"BIM = {bim:.2f} -> {classify_bim(bim)}")
print(f"(Paper reported BIM = 1.18, classified as high bursting liability)\n")

# F: paper reports Phi_sp = 1.5e-3, Phi_st = 6.5e-4
f = calculate_f(1.5e-3, 6.5e-4)
print(f"F = {f:.2f} -> {classify_f(f)}")
print(f"(Paper reported F = 2.32, classified as weak-to-medium shock)")



# ---------- Step 2: Compute stats from multiple specimens (not just use the reported mean) ----------
import numpy as np

# simulated individual specimen results (not in the paper, but realistic 
# given their reported mean 3.07 +/- 0.19 MPa from 6 UCT specimens)
uct_specimens = [2.89, 3.01, 3.15, 3.22, 2.95, 3.20]  # MPa, 6 specimens
brazilian_specimens = [0.38, 0.52, 0.41, 0.55, 0.36, 0.48]  # MPa, 6 specimens

sigma_c_mean = np.mean(uct_specimens)
sigma_c_std = np.std(uct_specimens, ddof=1)  # ddof=1 for sample std, matches how papers report it

sigma_t_mean = np.mean(brazilian_specimens)
sigma_t_std = np.std(brazilian_specimens, ddof=1)

print(f"\n=== Computed from individual specimens ===")
print(f"UCS: {sigma_c_mean:.2f} +/- {sigma_c_std:.2f} MPa (paper: 3.07 +/- 0.19 MPa)")
print(f"UTS: {sigma_t_mean:.2f} +/- {sigma_t_std:.2f} MPa (paper: 0.45 +/- 0.11 MPa)")

# now feed the computed mean into our existing B1 function
b1_from_computed = calculate_b1(sigma_c_mean, sigma_t_mean)
print(f"\nB1 using computed means = {b1_from_computed:.2f} -> {classify_b1(b1_from_computed)}")



# ---------- Step 3: Calculate R directly from a realistic curve using numerical integration ----------
# Note: illustrative curve using real peak stress (3.07 MPa); 
# validated R=1.3 comes from Step 1's literal paper values, not this curve

import matplotlib.pyplot as plt

# Build a more realistic asymmetric curve:
# - rises steeply to peak (like real rock loading)
# - drops MUCH faster after peak (brittle post-peak behavior, unlike our earlier symmetric curve)
strain_rise = np.linspace(0, 0.4, 100)      # pre-peak: strain 0 to 0.4%
stress_rise = 3.07 * (strain_rise / 0.4) ** 0.7  # curves up toward peak

strain_drop = np.linspace(0.4, 0.65, 60)    # post-peak: strain 0.4 to 0.65% (short = brittle)
stress_drop = 3.07 * (1 - ((strain_drop - 0.4) / 0.25) ** 1.5)  # steep drop

strain = np.concatenate([strain_rise, strain_drop])
stress = np.concatenate([stress_rise, stress_drop])

peak_index = np.argmax(stress)
peak_strain = strain[peak_index]
peak_stress = stress[peak_index]

strain_before = strain[:peak_index+1]
stress_before = stress[:peak_index+1]
strain_after = strain[peak_index:]
stress_after = stress[peak_index:]

# numerical integration: trapz estimates the area under a curve 
# by adding up thin trapezoid slices between data points
w_e_computed = np.trapezoid(stress_before, strain_before)
w_p_computed = np.trapezoid(stress_after, strain_after)

r_computed = calculate_r(w_e_computed, w_p_computed)

print(f"\n=== Step 3: R calculated from actual curve integration ===")
print(f"W_E (pre-peak area, computed) = {w_e_computed:.4f}")
print(f"W_P (post-peak area, computed) = {w_p_computed:.4f}")
print(f"R = {r_computed:.2f} -> {classify_r(r_computed)}")

# plot it
plt.plot(strain, stress, color='black', linewidth=2)
plt.fill_between(strain_before, stress_before, color='lightblue', alpha=0.6, label=f'W_E = {w_e_computed:.3f}')
plt.fill_between(strain_after, stress_after, color='salmon', alpha=0.6, label=f'W_P = {w_p_computed:.3f}')
plt.scatter([peak_strain], [peak_stress], color='red', zorder=5, label='Peak strength')
plt.xlabel('Strain (%)')
plt.ylabel('Stress (MPa)')
plt.title(f'Illustrative Curve (peak={peak_stress:.2f} MPa) — Method demo, R differs from validated Step 1 result')
plt.legend()
plt.show()



# ---------- Step 4: Mohr-Coulomb fitting from triaxial data ----------

# confining pressures from the paper's triaxial tests
sigma_3 = np.array([0, 1.5, 3, 4.5])  # MPa

# simulated sigma_1 (axial stress at failure) - realistic values consistent 
# with paper's reported c=1.06 MPa, phi=21.4 degrees, with small scatter
sigma_1 = np.array([3.11, 6.33, 9.56, 12.78])  # MPa

# linear regression: sigma_1 = intercept + slope * sigma_3
# np.polyfit fits a line (degree 1) and returns [slope, intercept]
slope, intercept = np.polyfit(sigma_3, sigma_1, 1)

kp = slope
sigma_c_fit = intercept

# back-calculate friction angle and cohesion from kp and sigma_c
phi_rad = np.arcsin((kp - 1) / (kp + 1))
phi_deg = np.degrees(phi_rad)
cohesion = sigma_c_fit / (2 * np.sqrt(kp))

print(f"\n=== Step 4: Mohr-Coulomb fit from triaxial data ===")
print(f"Fitted line: sigma_1 = {sigma_c_fit:.2f} + {kp:.2f} * sigma_3")
print(f"Friction angle (phi): {phi_deg:.1f} degrees (paper: 21.4 degrees)")
print(f"Cohesion (c): {cohesion:.2f} MPa (paper: 1.06 MPa)")

# plot the fit against the data points
plt.figure()
plt.scatter(sigma_3, sigma_1, color='blue', label='Test data', zorder=5)
sigma_3_line = np.linspace(0, 5, 50)
sigma_1_line = intercept + slope * sigma_3_line
plt.plot(sigma_3_line, sigma_1_line, color='red', label=f'Fit: σ1={sigma_c_fit:.2f}+{kp:.2f}σ3')
plt.xlabel('Confining pressure σ3 (MPa)')
plt.ylabel('Axial stress at failure σ1 (MPa)')
plt.title('Mohr-Coulomb Fit (σ1 vs σ3 method)')
plt.legend()
plt.show()
