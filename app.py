import re

class NodoAST:
    def __init__(self, tipo, valor=None, hijos=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = hijos if hijos else []
        self.atributo = None
    
    def __str__(self):
        return self._str_arbol()
    
    def _str_arbol(self, nivel=0):
        indent = "  " * nivel
        resultado = f"{indent}{self.tipo}"
        if self.valor is not None:
            resultado += f"({self.valor})"
        if self.atributo is not None:
            resultado += f" [{self.atributo}]"
        resultado += "\n"
        
        for hijo in self.hijos:
            resultado += hijo._str_arbol(nivel + 1)
        return resultado
    
    def dibujar_ascii(self):
        """Dibuja el árbol en un formato ASCII más legible.

        Usa conectores ├──, └── y │ para mostrar la estructura del árbol.
        Incluye tipo, valor y atributo (si existen) en cada nodo.
        """
        label = self._label()
        if not self.hijos:
            return label

        lines = [label]
        for i, hijo in enumerate(self.hijos):
            is_last = (i == len(self.hijos) - 1)
            lines.extend(hijo._ascii_lines("", is_last))
        return "\n".join(lines)
    
    def _dibujar_nodo(self):
        # Este método ya no se usa; se conserva por compatibilidad interna.
        return [self._label()]

    def _label(self):
        """Construye la etiqueta de un nodo: tipo(valor) [atributo]"""
        if self.valor is not None:
            label = f"{self.tipo}({self.valor})"
        else:
            label = f"{self.tipo}"

        if self.atributo is not None:
            label += f" [{self.atributo}]"
        return label

    def _ascii_lines(self, prefix, is_tail):
        """Genera líneas ASCII recursivas con prefijos y conectores.

        prefix: cadena que se antepone (espacios y/o '│   ' según niveles previos)
        is_tail: si el nodo es el último hijo del padre (usa '└──')
        """
        connector = "└── " if is_tail else "├── "
        lines = [prefix + connector + self._label()]
        if not self.hijos:
            return lines

        for i, hijo in enumerate(self.hijos):
            is_last = (i == len(self.hijos) - 1)
            child_prefix = prefix + ("    " if is_tail else "│   ")
            lines.extend(hijo._ascii_lines(child_prefix, is_last))
        return lines

class AnalizadorLexico:
    def __init__(self, texto):
        self.texto = texto
        self.posicion = 0
        self.token_actual = None
        self.avanzar()
    
    def avanzar(self):
        while self.posicion < len(self.texto) and self.texto[self.posicion].isspace():
            self.posicion += 1
        
        if self.posicion >= len(self.texto):
            self.token_actual = ('$', None)
            return
        
        char_actual = self.texto[self.posicion]
        
        if char_actual in '+-*/()':
            self.token_actual = (char_actual, char_actual)
            self.posicion += 1
        elif char_actual.isdigit():
            numero = ''
            while (self.posicion < len(self.texto) and 
                   (self.texto[self.posicion].isdigit() or self.texto[self.posicion] == '.')):
                numero += self.texto[self.posicion]
                self.posicion += 1
            self.token_actual = ('numero', float(numero))
        else:
            raise SyntaxError(f"Carácter inesperado: {char_actual}")

class TablaSimbolos:
    def __init__(self):
        self.simbolos = {}
    
    def agregar(self, nombre, tipo, valor):
        self.simbolos[nombre] = {'tipo': tipo, 'valor': valor}
    
    def obtener(self, nombre):
        return self.simbolos.get(nombre)
    
    def __str__(self):
        if not self.simbolos:
            return "Tabla de símbolos vacía"
        
        resultado = "Tabla de Símbolos:\n"
        resultado += "-" * 30 + "\n"
        for nombre, info in self.simbolos.items():
            resultado += f"{nombre}: {info['tipo']} = {info['valor']}\n"
        return resultado

class EDTS:
    def __init__(self, texto):
        self.lexico = AnalizadorLexico(texto)
        self.tabla_simbolos = TablaSimbolos()
        self.contador_temporal = 0
    
    def analizar(self):
        arbol = self.E()
        if self.lexico.token_actual[0] != '$':
            raise SyntaxError("Expresión incompleta")
        return arbol
    
    def E(self):
        """E → T E'"""
        nodo_T = self.T()
        nodo_Eprima = self.E_prima()
        
        if nodo_Eprima:
            # Combinar operaciones
            if nodo_Eprima.hijos:
                nodo_Eprima.hijos.insert(0, nodo_T)
                return nodo_Eprima
        return nodo_T
    
    def E_prima(self):
        """E' → + T E' | - T E' | ε"""
        if self.lexico.token_actual[0] in ['+', '-']:
            operador = self.lexico.token_actual[1]
            self.lexico.avanzar()
            nodo_T = self.T()
            nodo_Eprima = self.E_prima()
            
            nodo_operador = NodoAST('operador', operador)
            if nodo_Eprima and nodo_Eprima.hijos:
                # Ya hay una operación en curso
                nodo_operador.hijos = [nodo_Eprima.hijos[0], nodo_T]
                if nodo_Eprima.hijos[1:]:
                    nodo_operador.hijos.extend(nodo_Eprima.hijos[1:])
            else:
                nodo_operador.hijos = [nodo_T]
            
            return NodoAST('E\'', hijos=[nodo_operador])
        return None
    
    def T(self):
        """T → F T'"""
        nodo_F = self.F()
        nodo_Tprima = self.T_prima()
        
        if nodo_Tprima:
            if nodo_Tprima.hijos:
                nodo_Tprima.hijos.insert(0, nodo_F)
                return nodo_Tprima
        return nodo_F
    
    def T_prima(self):
        """T' → * F T' | / F T' | ε"""
        if self.lexico.token_actual[0] in ['*', '/']:
            operador = self.lexico.token_actual[1]
            self.lexico.avanzar()
            nodo_F = self.F()
            nodo_Tprima = self.T_prima()
            
            nodo_operador = NodoAST('operador', operador)
            if nodo_Tprima and nodo_Tprima.hijos:
                nodo_operador.hijos = [nodo_Tprima.hijos[0], nodo_F]
                if nodo_Tprima.hijos[1:]:
                    nodo_operador.hijos.extend(nodo_Tprima.hijos[1:])
            else:
                nodo_operador.hijos = [nodo_F]
            
            return NodoAST('T\'', hijos=[nodo_operador])
        return None
    
    def F(self):
        """F → ( E ) | número"""
        if self.lexico.token_actual[0] == '(':
            self.lexico.avanzar()
            nodo_E = self.E()
            if self.lexico.token_actual[0] != ')':
                raise SyntaxError("Se esperaba ')'")
            self.lexico.avanzar()
            return nodo_E
        elif self.lexico.token_actual[0] == 'numero':
            valor = self.lexico.token_actual[1]
            nodo = NodoAST('numero', valor)
            self.lexico.avanzar()
            return nodo
        else:
            raise SyntaxError(f"Se esperaba número o '(', se encontró: {self.lexico.token_actual[0]}")

    def decorar_arbol(self, nodo):
        """Calcula los atributos (valores) de cada nodo"""
        if nodo.tipo == 'numero':
            nodo.atributo = nodo.valor
            # Agregar a tabla de símbolos
            temp_name = f"t{self.contador_temporal}"
            self.contador_temporal += 1
            self.tabla_simbolos.agregar(temp_name, 'constante', nodo.valor)
        elif nodo.tipo == 'operador':
            # Decorar hijos primero
            for hijo in nodo.hijos:
                self.decorar_arbol(hijo)
            
            # Calcular valor basado en operador
            if len(nodo.hijos) >= 2:
                izquierdo = nodo.hijos[0].atributo
                derecho = nodo.hijos[1].atributo
                
                if nodo.valor == '+':
                    nodo.atributo = izquierdo + derecho
                elif nodo.valor == '-':
                    nodo.atributo = izquierdo - derecho
                elif nodo.valor == '*':
                    nodo.atributo = izquierdo * derecho
                elif nodo.valor == '/':
                    if derecho == 0:
                        raise ZeroDivisionError("División por cero")
                    nodo.atributo = izquierdo / derecho
                
                # Agregar resultado a tabla de símbolos
                temp_name = f"t{self.contador_temporal}"
                self.contador_temporal += 1
                self.tabla_simbolos.agregar(temp_name, 'temporal', nodo.atributo)

# Función principal de prueba
def main():
        expr = input("Ingrese una expresión matemática: ")
    
        try:
            edts = EDTS(expr)
            arbol = edts.analizar()
            edts.decorar_arbol(arbol)
            
            print("Árbol AST:")
            print(arbol)
            
            print("\nArte ASCII del árbol:")
            print(arbol.dibujar_ascii())
            
            print(f"\nResultado: {arbol.atributo}")
            print(edts.tabla_simbolos)
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()