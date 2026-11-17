package main

import "fmt"

/*
ALGORITMO GENERAL - PRACTICA DE SUSTENTACION (HIVOR)
Lexico: identificadores, palabras reservadas, literales, operadores y delimitadores.
Sintactico: var, const, arreglos, funciones normales, expresiones, if / else if / else,
            fmt.Println y referencias a variables/campos/indices.
Semantico: RS-1 (declaracion previa, indices, campos) y
           RS-3 (compatibilidad de tipos, const, colecciones, asignaciones, lectura).
*/

type Persona struct {
	nombre string
	edad   int
}

// Funcion convencional con dos parametros y retorno.
func calcularArea(base int, altura int) int {
	return base * altura
}

func main() {
	// Declaraciones explicitas, inferencia y constante.
	var edad int = 20
	var nombre string = "Ana"
	var promedio float64 = 9.5
	var activo bool = true
	var auxiliar int
	const limite int = 100
	var mensaje = nombre
	apodo := "Estudiante"

	// Arreglo, slice, mapa y acceso a campos de struct.
	var edades [3]int
	numeros := [3]int{10, 20, 30}
	notas := []int{7, 8, 9}
	edadesPorNombre := map[string]int{"Ana": 20, "Luis": 25}
	persona := Persona{nombre: "Ana", edad: 20}

	// Expresiones aritmeticas; prioridad de multiplicacion; llamada a funcion.
	var total int = 2 + 3*4
	area := calcularArea(numeros[0], 5)
	var saludo string = "Hola, " + nombre

	// RS-1 y RS-3: acceso valido y compatibilidad exacta.
	edad = 21
	edad += 2
	numeros[0] = 25
	notas[1] = 10
	edadesPorNombre["Ana"] = 21
	persona.edad = 23

	// Condicion, conjuncion, if, else if y else: siempre con llaves.
	if edad >= 18 && edad <= 60 {
		fmt.Println("Mayor de edad:", nombre)
	} else if edad >= 13 && edad <= 17 {
		fmt.Println("Adolescente:", nombre)
	} else {
		fmt.Println("Otra edad")
	}

	// Usos correctos de identificadores, indices y campos.
	fmt.Println(edad, nombre, promedio, activo, auxiliar, limite, mensaje, apodo)
	fmt.Println(edades[0], numeros[1], notas[1], edadesPorNombre["Ana"])
	fmt.Println(persona.nombre, persona.edad, total, area, saludo)

	// Lectura: el receptor debe existir y ser modificable.
	fmt.Scanln(&edad)
}
