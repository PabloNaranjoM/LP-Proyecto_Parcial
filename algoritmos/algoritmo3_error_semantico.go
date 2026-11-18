package main

/*
 * Algoritmo de Validación Semántica 3 (Avance 3 - Errores Semánticos)
 * ===================================================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Josué Pacheco (@JosuePach3co)
 *
 * Descripción:
 * Caso de prueba semántica con errores deliberados enfocados en RS-4
 * (operaciones permitidas) y RS-6 (estructuras de control).
 */

 import "fmt"
const LIMITE_MAXIMO int = 100
const ETIQUETA_FIJA string = "ESPOL"

func main() {
	var entero int = 15
	var decimal float64 = 4.5
	var texto string = "Compiladores"
	var bandera bool = true

	// =========================================================================
	// BLOQUE 1: ERRORES DE RS-4 (OPERACIONES PERMITIDAS)
	// =========================================================================

	// [Error RS-4 #1]: Suma entre tipos incompatibles ('int' + 'float64') sin coerción implícita.
	errSumaMixta := entero + decimal

	// [Error RS-4 #2]: Multiplicación entre tipos incompatibles ('int' * 'float64').
	errMultMixta := entero * decimal

	// [Error RS-4 #3]: Operador módulo '%' aplicado sobre operando 'float64'.
	errModuloFloat := decimal % 2.0

	// [Error RS-4 #4]: Operador lógico '&&' con operando izquierdo no booleano ('int').
	errAndNoBool := entero && bandera

	// [Error RS-4 #5]: Operador lógico '||' con operando derecho no booleano ('string').
	errOrNoBool := bandera || texto

	// [Error RS-4 #6]: Negación lógica '!' aplicada sobre tipo no booleano ('int').
	errNotNoBool := !entero

	// [Error RS-4 #7]: Comparación relacional '>' entre tipos distintos ('int' y 'float64').
	errCompRelacional := entero > decimal

	// [Error RS-4 #8]: Comparación de igualdad '==' entre tipos distintos ('int' y 'string').
	errCompIgualdad := entero == texto

	// [Error RS-4 #9]: Operador de incremento '++' aplicado sobre variable 'string'.
	texto++

	// [Error RS-4 #10]: Operador de decremento '--' aplicado sobre una constante ('const').
	LIMITE_MAXIMO--

	// =========================================================================
	// BLOQUE 2: ERRORES DE RS-6 (ESTRUCTURAS DE CONTROL)
	// =========================================================================

	// [Error RS-6 #11]: Condición de sentencia 'if' de tipo 'int' (se requiere 'bool').
	if entero {
		fmt.Println("Condición inválida en if")
	}

	// [Error RS-6 #12]: Condición de bucle 'for' de tipo 'float64' (se requiere 'bool').
	for decimal {
		fmt.Println("Condición inválida en for")
	}

	// [Error RS-6 #13 y #14]: Incompatibilidad de tipo entre tag de 'switch' ('int')
	// y cláusulas 'case' ('string' y 'bool').
	// [Error RS-6 #15]: Uso de 'continue' dentro de 'switch' sin bucle 'for' envolvente.
	switch entero {
	case "uno":
		continue
	case true:
		fmt.Println("Case booleano incompatible con selector int")
	default:
		fmt.Println("Caso por defecto")
	}

	// [Error RS-6 #16]: Uso de 'fallthrough' fuera de una estructura 'switch'.
	if bandera {
		fallthrough
	}

	// [Error RS-6 #17]: Uso de 'continue' fuera de cualquier bucle 'for'.
	continue

	// [Error RS-6 #18]: Uso de 'break' fuera de cualquier bucle 'for' o 'switch'.
	break
}