StreamView Analytics – Catálogo de Películas y Series

Proyecto de la asignatura **ADY1104 – Visualización de Datos** (DuocUC).
Análisis exploratorio y dashboard interactivo del catálogo de contenidos de una plataforma de streaming (películas y series, datos hasta 2025).

**Integrantes:** _[completar nombres del grupo]_
**Docente:** Alicia Ramos
**Dashboard (Looker Studio):** _[pegar enlace; permiso "cualquier persona con el enlace puede ver"]_

---

## 1. Objetivo

Entender cómo está compuesto el catálogo (volumen, géneros, países, idiomas), cómo se valora (calificación y popularidad) y qué películas resultan rentables (ROI), para entregar recomendaciones a las áreas de **Contenido, Marketing y Producción**.

**Alcance:** el análisis se limita a datos de catálogo. No se dispone de usuarios, reproducciones, suscripciones ni dispositivos, por lo que **no se calculan KPIs de retención ni engagement**.

## 2. Estructura del proyecto

```
├── data/          # CSV originales y datos limpios (catalogo_clean_dashboard.csv, kpis_generales.csv)
├── notebooks/     # EP2_Encargo_StreamView_corregido.ipynb (calidad, limpieza, KPIs, EDA, exportación)
├── dashboard/     # Capturas / referencia del dashboard de Looker Studio
├── images/        # Gráficos e imágenes usadas en informe, resumen e infografía
├── src/           # Código auxiliar (si aplica)
└── README.md
```

## 3. Datos de entrada

| Archivo | Contenido | Dimensión |
|---|---|---|
| `netflix_movies_detailed_up_to_2025.csv` | Películas | 16.000 × 18 |
| `netflix_tv_shows_detailed_up_to_2025.csv` | Series | 16.000 × 16 |

Ambos archivos están en `data/`. El notebook los lee con rutas relativas (`../data/`), por lo que se ejecuta desde `notebooks/` sin modificaciones.

## 4. Cómo reproducir

1. Requisitos: Python 3.9+ con `pandas`, `numpy`, `matplotlib`, `seaborn` y `jupyter`.
   ```bash
   pip install pandas numpy matplotlib seaborn jupyter
   ```
2. Abrir `notebooks/EP2_Encargo_StreamView_corregido.ipynb` y ejecutar todas las celdas (o `cd notebooks && jupyter nbconvert --to notebook --execute --inplace EP2_Encargo_StreamView_corregido.ipynb`).
4. Salidas generadas:
   - `data/catalogo_clean_dashboard.csv` → 31.991 filas × 20 columnas (fuente del dashboard).
   - `data/kpis_generales.csv` → KPIs generales.
5. Cargar `catalogo_clean_dashboard.csv` en Looker Studio para reconstruir el dashboard.

## 5. Contenido del notebook

1. **Carga** de las dos fuentes.
2. **Calidad de datos:** nulos, duplicados, `show_id` no es clave global, coherencia entre `rating` y `vote_average`, tipo/duración, coherencia de presupuesto e ingresos.
3. **Limpieza e integración:** unión de películas y series, homologación de géneros y países.
4. **KPIs.**
5. **EDA:** composición del catálogo, popularidad y calificación, evolución temporal, rentabilidad.
6. **Exportación** de los datos para el dashboard.

## 6. Decisiones de datos relevantes

- **Clave de unión:** `show_id` + `type` (el `show_id` solo no es único entre películas y series).
- **Calificación:** se calcula solo sobre títulos calificados (`vote_count > 0`). Quedan sin calificar el 22,9 % de las series y el 5,6 % de las películas.
- **ROI** = (ingresos − presupuesto) / presupuesto. Se reporta la **mediana (0,70)** sobre las **3.540 películas** con datos financieros; la media (~780) se distorsiona por valores atípicos. Las series no tienen presupuesto ni ingresos, por lo que no tienen ROI.
- **Géneros** homologados entre películas y series. Documentary se excluye del análisis de ROI por tamaño muestral insuficiente (n = 22).
- **Países:** abreviaturas para legibilidad (USA, UK, S. Korea, UAE, etc.); "No especificado" no cuenta como país.
- **Campos derivados:** `rango_calificacion` (rangos 0–2, 2–4, 4–5, 5–6, 6–7, 7–8, 8–9, 9–10), `tipo_es` (Películas / Series), `calificado`, `tiene_datos_financieros`, `roi`.

## 7. Dashboard (Looker Studio)

Tres páginas:

1. **Visión general del catálogo:** KPIs, evolución por año de estreno, géneros y países principales, rangos de calificación.
2. **Series vs películas:** comparación de calificación y popularidad, y evolución anual.
3. **Recomendaciones:** acciones por área (Contenido, Marketing, Producción) apoyadas en los datos.

Incluye filtro por año de estreno y botones de navegación entre páginas.

## 8. Hallazgos principales

- Catálogo equilibrado: **16.000 películas y 15.991 series** (31.991 títulos); 122 países productores principales (147 si se cuentan todos los países listados por título).
- Calificación promedio (títulos calificados): **6,63** global; **series 7,02 vs películas 6,31**.
- Popularidad (títulos calificados): series 70,4 vs películas 20,9. A partir de **2024** las películas superan a las series (75,7 vs 73,1) y la brecha se amplía en 2025 (96,6 vs 62,8).
- **ROI mediano de películas: 0,70.** Terror destaca por su baja inversión (presupuesto mediano ≈ 6,2 M frente a 32–59 M en Acción, Aventura y Fantasía).

## 9. Limitaciones

- Sin datos de usuarios ni consumo: no hay KPIs de retención, engagement ni suscripciones.
- La popularidad no es directamente comparable entre series y películas (hipótesis: depende de la fecha de estreno).
- Porcentaje relevante de títulos sin calificación; el ROI solo existe para películas con presupuesto e ingresos informados.
- Muestras pequeñas en algunos géneros al analizar ROI.

## 10. Entregables del proyecto

Informe ejecutivo (PDF), dashboard (enlace), resumen ejecutivo (PDF/PPT), infografía y esta carpeta de proyecto.
