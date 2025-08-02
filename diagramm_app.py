import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import streamlit as st

st.set_page_config(page_title="Ungleichungsdiagramm", layout="centered")
st.title("📊 Entscheidungsdiagramm")

# Slider für Parameter
p_foto = st.slider(
    '📷 Wahrscheinlichkeit (p), dass das Vorliegende ein echtes Foto ist.',
    min_value=0.0, max_value=1.0, step=0.01, value=0.5
)
O_Täuschung = st.slider(
    '🎭 Kosten für die Täuschung (c) (niedrige Werte = Täuschung soll unbedingt vermieden werden).',
    min_value=-20.0, max_value=0.0, step=0.5, value=-10.0
)

# Definitionsbereich
a_vals = np.linspace(0, 15, 400)
b_vals = np.linspace(-15, 15, 400)
A, B = np.meshgrid(a_vals, b_vals)

# Parameter
c = O_Täuschung
p = p_foto
a = A
b = B

# Ungleichung
lhs = p * (2 * a - c - b)
rhs = a - c
inequality = lhs > rhs

# Gültigkeitsbedingungen
epsilon = 2
well_defined = (b >= -2) & (b <= 2)
well_defined &= (c < 0) & (c < b - epsilon)
well_defined &= (a > 0) & (a > b + epsilon)

# Farbcodierung
region = np.zeros_like(a, dtype=int)
region[well_defined] = 1
region[inequality & well_defined] = 2
cmap = mcolors.ListedColormap(['gray', 'red', 'green'])

# Plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.contourf(a, b, region, levels=[-0.5, 0.5, 1.5, 2.5], cmap=cmap)
ax.set_xlabel('Belohnung Korrekte Klassifizierung (a)')
ax.set_ylabel('Auszahlung Versäumnis (b)\n Kann je nach Situation/Individuum positiv oder negativ sein.')
ax.set_title(r'Definitionsbereich der Ungleichung: $p(foto)(2a - c - b) > a - c$.')

ax.grid(True, linestyle='--', linewidth=0.5)

# Textbox 
ax.text(
    0.1, 11,  # x- und y-Position im Diagramm
    'Aus dem Schnittpunkt der gewählten Werte für a und b ergibt sich die rationale Stratgie.\nGrüner Bereich = Ungleichung ist erfüllt; Klassifizierung als echtes Foto ist rational (höherer Erwarungswert).\nRoter Bereich = Ungleichung nicht erfüllt; Klassifizierung als KI-Erzeugniss ist rational. \nGrauer Bereich = nicht definiert.',
    fontsize=8,
    color='black',
    bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5')
)
 
# Legende
legend_patches = [
    mpatches.Patch(color='green', label='gültig & erfüllt = Klassifizierung als Foto'),
    mpatches.Patch(color='red', label='gültig & nicht erfüllt = Klassifizierung als KI-Erzeugniss'),
    mpatches.Patch(color='gray', label='nicht definiert')
]
ax.legend(handles=legend_patches, loc='lower right')

ax.set_xticks(np.arange(0, 16, 1))
ax.set_yticks(np.arange(-15, 16, 1))

st.pyplot(fig)
