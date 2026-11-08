package main

/*
 * Algoritmo de Validación Sintáctica 1 (Avance 2 - Errores Sintácticos)
 * =====================================================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Pablo Naranjo (@PabloNaranjoM)
 */

import "fmt"

type Estudiante struct {
	nombre    string
	matricula int
}

func main() {
	edad := 20
	fmt.Scanln(&edad)

	// Error sintáctico 1: declaración corta ':=' sin expresión a la derecha
	tasa := ;

	// Error sintáctico 2: paréntesis sin cerrar en expresión con división y módulo
	residuo := (edad / 2 % 3;

	// Error sintáctico 3: operador relacional sin operando derecho en condición
	esMayor := edad >= ;
}
