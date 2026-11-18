package main

/*
 * Algoritmo Completo 2 (Válido) - Avance Final
 * ============================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Hivor Araujo (@AraujoHivor)
 *
 * Descripción:
 * Programa completo y válido en Go que integra los aportes léxicos,
 * sintácticos y semánticos (RS-1 y RS-3) de Hivor Araujo:
 * - Léxico: palabras reservadas base, string, Println, identificadores,
 *   enteros, operadores aritméticos (+, -, *, /, %), '=' y delimitadores (), {}, [].
 * - Sintáctico: var tipada/sin valor, const, arreglos [n]T, referencias/índices,
 *   funciones con y sin retorno, return, if/else if/else y fmt.Println.
 * - Semántico: declaración previa, índices y campos (RS-1); compatibilidad estricta
 *   de tipos, inmutabilidad de const, colecciones, struct_init y lectura (RS-3).
 */

import "fmt"

type Persona struct {
	nombre string
	edad   int
}

// Función con retorno explícito
func calcularArea(base int, altura int) int {
	return base * altura
}

// Función sin retorno explícito (void)
func mostrarResumen(nombre string, area int) {
	fmt.Println("Usuario:", nombre, "| Área:", area)
	return
}

func main() {
	// Declaraciones explícitas, sin valor inicial, con inferencia y constante
	var edad int = 20
	var nombre string = "Ana"
	var activo bool = true
	var auxiliar int
	const limite int = 100
	var mensaje = nombre
	apodo := "Estudiante"

	// Arreglos, slice, mapa y struct
	var edades [3]int
	numeros := [3]int{10, 20, 30}
	lista := []int{1, 2, 3}
	edadesPorNombre := map[string]int{"Ana": 20, "Luis": 25}
	persona := Persona{nombre: "Ana", edad: 20}

	// Expresiones aritméticas, llamadas a funciones y asignaciones válidas
	var total int = 2 + 3*4
	area := calcularArea(numeros[0], 5)
	edad = 21
	edad += 2
	numeros[0] = 25
	lista[1] = 10
	edadesPorNombre["Ana"] = 22
	persona.edad = 23

	// Condicional if / else if / else con llaves obligatorias
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
		mostrarResumen(nombre, area)
	}

	// Usos válidos de identificadores, índices y campos (RS-1)
	fmt.Println(edad, auxiliar, limite, mensaje, apodo)
	fmt.Println(edades[0], numeros[1], lista[1], edadesPorNombre["Ana"])
	fmt.Println(persona.nombre, persona.edad, total)

	// Lectura sobre variable modificable (RS-3)
	fmt.Scanln(&edad)
}
