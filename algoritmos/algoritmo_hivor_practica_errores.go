package main

import "fmt"

/*
BANCO DE ERRORES PARA PRACTICAR TU SUSTENTACION (HIVOR)
*/

type Persona struct {
	nombre string
	edad   int
}

func sumar(a int, b int) int {
	return a + b
}

// S11 - Falta ')' al cerrar los parametros de una funcion.
// Descomenta esta linea FUERA de main para probarlo.
// func sumarMal(a int, b int { return a + b }

func main() {
	var edad int = 20
	var nombre string = "Ana"
	const limite int = 100
	numeros := [3]int{10, 20, 30}
	lista := []int{1, 2, 3}
	edades := map[string]int{"Ana": 20}
	persona := Persona{nombre: "Ana", edad: 20}
	total := sumar(2, 3)
	fmt.Println(edad, nombre, limite, numeros[0], lista[0], edades["Ana"], persona.nombre, total)

	// ==============================================================
	// NIVEL 1: ERRORES LEXICOS
	// El lexer encuentra un caracter no reconocido.
	// ==============================================================

	// L1 - '@' no es un token de este subconjunto de Go.
	// edad = 20 @

	// L2 - '$' no forma parte de los identificadores permitidos.
	// edad = 20 $

	// L3 - '#' es un caracter no reconocido en este contexto.
	// edad = 20 #

	// ==============================================================
	// NIVEL 2: ERRORES SINTACTICOS
	// Todos sus signos pueden ser tokens; el orden es incorrecto.
	// ==============================================================

	// S1 - Falta la expresion despues del signo igual.
	// var nuevaEdad int = ;

	// S2 - Falta cerrar el corchete ']' del arreglo.
	// var copia [3 int

	// S3 - Dos operadores binarios seguidos, falta un operando.
	// var suma int = edad + * 5

	// S4 - Condicion if incompleta: no existe operando despues de &&.
	// if edad >= 18 && { fmt.Println("Hola") }

	// S5 - Falta el bloque con llaves del if.
	// if edad >= 18 fmt.Println("Adulto")

	// S6 - Falta la coma entre dos argumentos de Println.
	// fmt.Println("Edad:" edad)

	// S7 - Coma final sin un argumento posterior en Println.
	// fmt.Println("Hola",)

	// S8 - Falta cerrar el parentesis de Println.
	// fmt.Println("Hola"

	// S9 - Uso de 'while' como si fuera estructura de control de Go.
	// En Go no hay una palabra reservada 'while': se usa 'for'.
	// while edad < 25 { edad = edad + 1 }

	// S10 - Una asignacion requiere una expresion a la derecha.
	// edad = ;

	// ==============================================================
	// NIVEL 3: ERRORES SEMANTICOS RS-1 (IDENTIFICADORES)
	// El parser reconoce la sintaxis, pero la referencia es incorrecta.
	// ==============================================================

	// R1 - 'fantasma' no ha sido declarado antes de usarse.
	// fantasma = 10

	// R2 - Se usa una variable no declarada dentro de Println.
	// fmt.Println(desconocido)

	// R3 - Indice de arreglo: debe ser int, no string.
	// numeros["uno"] = 10

	// R4 - Indice de slice: debe ser int, no string.
	// lista["primero"] = 5

	// R5 - Clave de mapa: debe ser string, no int.
	// edades[3] = 25

	// R6 - Campo de struct que no existe.
	// persona.altura = 170

	// R7 - Lectura sobre variable inexistente.
	// fmt.Scanln(&desconocido)

	// ==============================================================
	// NIVEL 3: ERRORES SEMANTICOS RS-3 (TIPOS, CONSTANTES)
	// El codigo tiene forma valida, pero viola compatibilidad o mutabilidad.
	// ==============================================================

	// T1 - String asignado a una variable int.
	// edad = "veinte"

	// T2 - Declaracion explicita con tipos incompatibles.
	// var puntaje int = "alto"

	// T3 - Un valor float64 se asigna a int, sin conversion explicita.
	// edad = 20.5

	// T4 - No se puede modificar una constante.
	// limite = 200

	// T5 - No se puede leer sobre una constante.
	// fmt.Scanln(&limite)

	// T6 - El arreglo int recibe un elemento string.
	// otrosNumeros := [3]int{1, "dos", 3}

	// T7 - El slice int recibe un elemento string.
	// otraLista := []int{1, "dos", 3}

	// T8 - El mapa string -> int recibe un valor string.
	// otroMapa := map[string]int{"Ana": "veinte"}

	// T9 - El campo edad del struct Persona es int, no string.
	// otraPersona := Persona{nombre: "Ana", edad: "veinte"}

	// T10 - No puede inferirse int y luego asignar string.
	// edadInferida := 20
	// edadInferida = "veinte"
	// Para T10 descomenta LAS DOS lineas anteriores juntas.
}
