package main

/*
 * Algoritmo Completo 3 con Errores - Avance Final
 * ===============================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Josué Pacheco (@JosuePach3co)
 *
 * Descripción:
 * Reúne errores léxicos, sintácticos y semánticos (RS-4 y RS-6) en un solo
 * archivo de prueba, manteniendo llaves balanceadas en errores sintácticos para
 * que las tres fases de diagnóstico se ejecuten en una sola corrida.
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
	// 1. ERRORES LÉXICOS DELIBERADOS (@, $, ~, #)
	// =========================================================================
	var errorAcceso@ bool = false
	var sensorFallo$ bool = true
	var umbral~ int = 100
	var tokenRoto# bool = false

	// =========================================================================
	// 2. ERRORES SINTÁCTICOS RECUPERABLES
	// =========================================================================
	fmt.Print("Promedio:", decimal, );
	decimal -= ;
	bandera = (decimal > 2.0) && ;

	// =========================================================================
	// 3. ERRORES SEMÁNTICOS RS-4 (OPERACIONES PERMITIDAS)
	// =========================================================================
	// [Error RS-4 #1]: Suma entre tipos incompatibles ('int' + 'float64').
	errSumaMixta := entero + decimal

	// [Error RS-4 #2]: Multiplicación entre tipos incompatibles ('int' * 'float64').
	errMultMixta := entero * decimal

	// [Error RS-4 #3]: Operador módulo '%' aplicado sobre 'float64'.
	errModuloFloat := decimal % 2.0

	// [Error RS-4 #4]: Operador lógico '&&' con operando no booleano ('int').
	errAndNoBool := entero && bandera

	// [Error RS-4 #5]: Operador lógico '||' con operando no booleano ('string').
	errOrNoBool := bandera || texto

	// [Error RS-4 #6]: Negación lógica '!' sobre 'int'.
	errNotNoBool := !entero

	// [Error RS-4 #7]: Comparación relacional '>' entre 'int' y 'float64'.
	errCompRelacional := entero > decimal

	// [Error RS-4 #8]: Comparación de igualdad '==' entre 'int' y 'string'.
	errCompIgualdad := entero == texto

	// [Error RS-4 #9]: Incremento '++' sobre 'string'.
	texto++

	// [Error RS-4 #10]: Decremento '--' sobre constante ('const').
	LIMITE_MAXIMO--

	// =========================================================================
	// 4. ERRORES SEMÁNTICOS RS-6 (ESTRUCTURAS DE CONTROL)
	// =========================================================================
	// [Error RS-6 #11]: Condición de 'if' tipo 'int' (se requiere 'bool').
	if entero {
		fmt.Println("Condición inválida en if")
	}

	// [Error RS-6 #12]: Condición de 'for' tipo 'float64' (se requiere 'bool').
	for decimal {
		fmt.Println("Condición inválida en for")
	}

	// [Error RS-6 #13, #14 y #15]: Incompatibilidad en 'case' y 'continue' dentro de 'switch'.
	switch entero {
	case "uno":
		continue
	case true:
		fmt.Println("Case booleano incompatible con selector int")
	default:
		fmt.Println("Caso por defecto")
	}

	// [Error RS-6 #16]: 'fallthrough' fuera de 'switch'.
	if bandera {
		fallthrough
	}

	// [Error RS-6 #17]: 'continue' fuera de bucle 'for'.
	continue

	// [Error RS-6 #18]: 'break' fuera de bucle 'for' o 'switch'.
	break

	fmt.Println(errorAcceso, sensorFallo, umbral, tokenRoto)
}
