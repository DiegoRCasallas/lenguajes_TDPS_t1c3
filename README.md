# Analizador y Árbol AST (Lenguajes y Transducción)

Autor: Diego René Casallas Diaz.

Proyecto educativo que implementa un analizador sintáctico descendente para expresiones aritméticas, construye un árbol AST, decora el árbol calculando atributos (valores) y muestra el resultado junto con una tabla de símbolos.

## Archivos principales

- `app.py`: Analizador léxico y sintáctico (EDTS), construcción del AST, decoración de atributos y presentación (impresión del árbol y dibujo ASCII). Este script solicita la expresión mediante `input()` y muestra automáticamente el árbol, el arte ASCII, el resultado y la tabla de símbolos.

## Gramática (informal)

La gramática que analiza el programa es la clásica para expresiones aritméticas con precedencia y paréntesis:

E  → T E'

## Conjuntos FIRST
```
FIRST = {

## Conjuntos FOLLOW
```
FOLLOW = {

## Tabla de predicción (PREDICT) — simplificada
```
PREDICT = {

## Uso

1. Ejecutar el script con Python 3 (no requiere dependencias externas):

## Ejemplo de ejecución

Entrada: `3 + 4 * 2`

## Errores y limitaciones conocidas

- El analizador acepta sólo números (enteros o con punto decimal), operadores `+ - * /` y paréntesis `()`.

## Contribuciones y mejoras sugeridas

- Agregar soporte para variables y asignaciones.

## Licencia
Proyecto educativo — usar y modificar libremente para fines didácticos.

---
Fecha: 2025-11-12

Autor: Diego René Casallas Diaz.