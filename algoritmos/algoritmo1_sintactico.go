package main

/*
 * Algoritmo de Validación Sintáctica 1 (Avance 2 - Caso Válido)
 * =============================================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Pablo Naranjo (@PabloNaranjoM)
 */

import "fmt"

type Estudiante struct {
	nombre    string
	matricula int
	promedio  float64
}

func sumarPuntos(valores ...int) int {
	total := 0
	for _, v := range valores {
		total = total + v
	}
	return total
}

func main() {
	nombre := "Carlos"
	edad := 20
	bloqueado := false

	fmt.Scanln(&nombre, &edad)

	inventario := map[string]int{
		"teclados":  15,
		"monitores": 8,
	}

	alumno := Estudiante{
		"nombre":    nombre,
		"matricula": 202601,
		"promedio":  9.25,
	}

	residuo := (edad + 10) / 3 % 2
	accesoValido := !bloqueado && edad >= 18

	contador := 0
	for contador < 3 {
		contador = contador + 1
	}

	acumulado := 0
	for i := 0; i < 4; i++ {
		acumulado += i
	}

	totalPuntos := sumarPuntos(10, 20, 30)
	fmt.Println(alumno.nombre, inventario["teclados"], residuo, accesoValido, acumulado, totalPuntos)
}
