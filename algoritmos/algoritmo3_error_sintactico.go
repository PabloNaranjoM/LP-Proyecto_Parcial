package main

/*
 * Algoritmo de Validación Sintáctica 3 (Avance 2 - Errores Sintácticos)
 * =====================================================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Josué Pacheco (@JosuePach3co)
 */

import "fmt"

func main() {
	var promedio = 9.45
	var activo bool = true

	// Error sintáctico 1: llamada a fmt.Print con coma sin argumento final
	fmt.Print("Promedio:", promedio, );

	// Error sintáctico 2: asignación compuesta '-=' sin expresión a la derecha
	promedio -= ;

	// Error sintáctico 3: expresión lógica con conjunción '&&' sin operando derecho
	activo = (promedio > 8.0) && ;
}
