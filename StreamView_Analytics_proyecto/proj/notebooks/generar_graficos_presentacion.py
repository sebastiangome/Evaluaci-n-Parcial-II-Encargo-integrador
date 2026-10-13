import os
import pandas as pd
import matplotlib.pyplot as plt

# Directorio de imágenes relativo
os.makedirs('../images', exist_ok=True)

# Paleta y estilo visual oscuro para presentación
BG, TX, GR, RED, BL = '#0B1220', '#E8ECF4', '#2A3550', '#F0434B', '#4DA3FF'
plt.rcParams.update({'text.color': TX, 'axes.labelcolor': TX, 'xtick.color': TX, 'ytick.color': TX})
coma = lambda v: f"{v:.2f}".replace('.', ',')

def base(w, h):
    f, a = plt.subplots(figsize=(w, h), dpi=160)
    f.patch.set_facecolor(BG)
    a.set_facecolor(BG)
    for s in ['top', 'right']:
        a.spines[s].set_visible(False)
    for s in ['left', 'bottom']:
        a.spines[s].set_color(GR)
    return f, a

# Cargar catálogo limpio
csv_path = '../data/catalogo_clean_dashboard.csv'
if not os.path.exists(csv_path):
    csv_path = 'data/catalogo_clean_dashboard.csv'

df = pd.read_csv(csv_path)
r = df[(df.vote_count > 0) & df.release_year.between(2010, 2025)]

# Gráficos 1 y 2: Calificación y Popularidad
for col, nombre, titulo, ylab in [
    ('vote_average', 'h1_calificacion_por_anio', 'Calificación promedio por año de estreno', 'Calificación (0-10)'),
    ('popularity', 'h1_popularidad_por_anio', 'Popularidad promedio por año de estreno', 'Popularidad')
]:
    p = r.pivot_table(index='release_year', columns='type', values=col, aggfunc='mean')
    f, a = base(10, 5)
    a.grid(axis='y', color=GR, lw=.6)
    a.set_axisbelow(True)
    a.plot(p.index, p['TV Show'], color=BL, lw=3, marker='o', label='Series')
    a.plot(p.index, p['Movie'], color=RED, lw=3, marker='o', label='Películas')
    a.set_xticks(p.index)
    a.tick_params(axis='x', labelsize=9)
    a.set_ylabel(ylab)
    a.set_title(titulo, loc='left', fontsize=15, fontweight='bold', pad=14)
    if col == 'vote_average':
        a.set_ylim(5.5, 8)
    else:
        a.axvline(2023.5, color=TX, ls='--', lw=1, alpha=.6)
    a.legend(frameon=False, fontsize=11)
    f.tight_layout()
    img_out = f'../images/{nombre}.png' if os.path.exists('../images') else f'images/{nombre}.png'
    f.savefig(img_out, facecolor=BG)
    plt.close(f)
    print(f"Generado: {img_out}")

# Gráfico 3: ROI mediano por género
fin = df[df.tiene_datos_financieros.astype(str).isin(['True', '1', 'Sí', 'True'])]
g = fin.groupby('genero_principal').roi.agg(['median', 'count'])
g = g[g['count'] >= 50].sort_values('median')

f, a = base(10, 6)
a.grid(axis='x', color=GR, lw=.6)
a.set_axisbelow(True)
b = a.barh(
    [f"{i} (n={int(n)})" for i, n in zip(g.index, g['count'])],
    g['median'],
    color=[RED if i in ('Horror', 'Animation') else '#5B6B8C' for i in g.index]
)

for rect, v in zip(b, g['median']):
    a.text(v + .03, rect.get_y() + rect.get_height() / 2, coma(v), va='center', fontsize=10, fontweight='bold')

a.axvline(0.70, color=TX, ls='--', lw=1)
a.set_xlabel('ROI mediano')
a.set_title('ROI mediano por género · películas con datos financieros', loc='left', fontsize=14, fontweight='bold', pad=14)
f.tight_layout()
roi_out = '../images/h2_roi_por_genero.png' if os.path.exists('../images') else 'images/h2_roi_por_genero.png'
f.savefig(roi_out, facecolor=BG)
plt.close(f)
print(f"Generado: {roi_out}")

print("¡Todos los gráficos fueron generados con éxito!")
