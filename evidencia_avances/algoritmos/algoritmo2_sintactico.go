package main

/*
 * Algoritmo de Validación Sintáctica 2 (Avance 2 - Caso Válido)
 * =============================================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Hivor Araujo (@AraujoHivor)
 */

import "fmt"

func calcularArea(base int, altura int) int {
	return base * altura
}

func main() {
	var edad int = 25
	var nombre string = "Ana"
	var activo bool = true
	var factor float64 = 1.5
	var auxiliar int

	var edades [3]int
	numeros := [3]int{10, 20, 30}

	var total int = 2 + 3 * 4
	var area int = calcularArea(numeros[0], 5)

	if edad >= 18 && edad <= 60 {
		var estado string = "Adulto"
		fmt.Println("Categoría:", estado)
	} else if edad >= 13 && edad <= 17 {
		var estado string = "Adolescente"
		fmt.Println("Categoría:", estado)
	} else {
		var estado string = "Menor"
		fmt.Println("Categoría:", estado)
	}

	if activo && area > 10 {
		fmt.Println("Usuario:", nombre, "Área:", area, "Total:", total, factor, edades[0], auxiliar)
	} else {
		fmt.Println("Inactivo")
	}
}
