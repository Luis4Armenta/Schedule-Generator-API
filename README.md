# Generador de horarios UPIICSA API

Se trata de una API desarrollada en FastAPI que emplea web scraping para extraer horarios del SAES (Secuencias formadas por diferentes unidades de aprendizaje, mismas que tienen un profesor asignado, con diferentes sesiones a la semana) y comentarios sobre los profesores que las imparten. El generador de horarios utiliza estos datos extraídos de la web para generar todos los posibles horarios mediante un algoritmo de backtracking y puntuarlos de acuerdo al agrado que los alumnos han manifestado en comentarios sobre los profesores que integran cada uno de los horarios.

### Características

- Extrae horarios de clase de documentos HTML exportados del SAES.
- Genera todas las posibles combinaciones de materias de acuerdo a los parámetros dados (Hora de entrada, hora de salida, límite de créditos, materias obligatorias, exclusión de profesores, etc).
- Extrae comentarios automáticamente del diccionario de maestros.
- Realiza análisis de sentimiento sobre comentarios de profesores.
- Asigna una puntuación positiva a los profesores según los comentarios que en el diccionario de maestros se hayan.
- Ordena los horarios generados según la puntuación positiva.