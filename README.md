# Analizador y Árbol AST (Lenguajes y Transducción)

Autor: Diego René Casallas Diaz.

Proyecto educativo que implementa un analizador sintáctico descendente para expresiones aritméticas, construye un árbol AST, decora el árbol calculando atributos (valores) y muestra el resultado junto con una tabla de símbolos.

## Archivos principales

- `app.py`: Analizador léxico y sintáctico (EDTS), construcción del AST, decoración de atributos y presentación (impresión del árbol y dibujo ASCII). Este script solicita la expresión mediante `input()` y muestra automáticamente el árbol, el arte ASCII, el resultado y la tabla de símbolos.

## Gramática (informal)

La gramática que analiza el programa es la clásica para expresiones aritméticas con precedencia y paréntesis:

E  → T E'

## Gramática con atributos

```
E  → E₁ + T    { E.valor = E₁.valor + T.valor }
E  → E₁ - T    { E.valor = E₁.valor - T.valor }
E  → T         { E.valor = T.valor }

T  → T₁ * F    { T.valor = T₁.valor * F.valor }
T  → T₁ / F    { T.valor = T₁.valor / F.valor }
T  → F         { T.valor = F.valor }

F  → ( E )     { F.valor = E.valor }
F  → número    { F.valor = número.valor }
```

## Conjuntos FIRST
```
FIRST = {

    'E': ['(', 'numero'],
    'T': ['(', 'numero'],
    'F': ['(', 'numero']
}


```
## Conjuntos FOLLOW
```
FOLLOW = {'E': ['$', '+', '-', ')'],
    'T': ['$', '+', '-', '*', '/', ')'],
    'F': ['$', '+', '-', '*', '/', ')']
}
```
## Tabla de predicción (PREDICT) — simplificada
```
PREDICT = {
    ('E', '('): ['T', 'E\''],
    ('E', 'numero'): ['T', 'E\''],
    ('E\'', '+'): ['+', 'T', 'E\''],
    ('E\'', '-'): ['-', 'T', 'E\''],
    ('E\'', '$'): ['ε'],
    ('E\'', ')'): ['ε'],
    ('T', '('): ['F', 'T\''],
    ('T', 'numero'): ['F', 'T\''],
    ('T\'', '*'): ['*', 'F', 'T\''],
    ('T\'', '/'): ['/', 'F', 'T\''],
    ('T\'', '+'): ['ε'],
    ('T\'', '-'): ['ε'],
    ('T\'', '$'): ['ε'],
    ('T\'', ')'): ['ε'],
    ('F', '('): ['(', 'E', ')'],
    ('F', 'numero'): ['numero']
}

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