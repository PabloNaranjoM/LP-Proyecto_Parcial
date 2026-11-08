package main

/*
 * Algoritmo de Validación Sintáctica 2 (Avance 2 - Errores Sintácticos)
 * =====================================================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Hivor Araujo (@AraujoHivor)
 */

import "fmt"

func main() {
	var edad int = 25
	notas := [3]int{10, 9, 8}

	// Error sintáctico 1: declaración explícita 'var' sin expresión tras '='
	var limite int = ;

	// Error sintáctico 2: declaración de arreglo sin corchete de cierre ']'
	var edades [3 int;

	// Error sintáctico 3: expresión aritmética incompleta con doble operador
	var suma int = edad + * 5;
}
