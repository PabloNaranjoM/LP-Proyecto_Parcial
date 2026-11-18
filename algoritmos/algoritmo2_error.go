package main

/*
 * Algoritmo Completo 2 con Errores - Avance Final
 * ===============================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Hivor Araujo (@AraujoHivor)
 *
 * Descripción:
 * Reúne errores léxicos, sintácticos y semánticos (RS-1 y RS-3) en un solo
 * archivo de prueba. Los errores sintácticos usan recuperación con ';' sin
 * desbalancear llaves para que el análisis semántico también se ejecute.
 */

import "fmt"

type Persona struct {
	nombre string
	edad   int
}

func main() {
	var edad int = 20
	const limite int = 100
	numeros := [3]int{10, 20, 30}
	lista := []int{1, 2, 3}
	edades := map[string]int{"Ana": 20}
	persona := Persona{nombre: "Ana", edad: 20}

	// =========================================================================
	// 1. ERRORES LÉXICOS DELIBERADOS (@, $, ?, #)
	// =========================================================================
	var precio@ int = 12
	var descuento$ int = 3
	var codigo? int = 7
	var marca# int = 5

	// =========================================================================
	// 2. ERRORES SINTÁCTICOS RECUPERABLES
	// =========================================================================
	var limiteMal int = ;
	var edadesMal [3 int;
	var sumaMal int = edad + * 5;
	fmt.Println("Hola",);
	edad = ;

	// =========================================================================
	// 3. ERRORES SEMÁNTICOS (RS-1 y RS-3)
	// =========================================================================
	// RS-3: Asignar string a una variable int
	edad = "veinte"

	// RS-3: Intentar modificar una constante
	limite = 200

	// RS-1: Utilizar una variable no declarada
	fantasma = 10

	// RS-1: Índice incorrecto en un arreglo
	numeros["uno"] = 99

	// RS-1: Campo inexistente en una estructura
	persona.altura = 175

	// RS-1: Clave incorrecta en un mapa
	edades[1] = 30

	// RS-3: Elementos incompatibles en un slice
	incorrectos := []int{10, "texto"}

	// RS-3: Tipo incorrecto en un campo del struct
	otraPersona := Persona{nombre: "Luis", edad: "veinte"}

	// RS-3: Intentar leer datos sobre una constante
	fmt.Scanln(&limite)

	fmt.Println(precio, descuento, codigo, marca, lista[0])
}
