package main

/*
 * Algoritmo de Validación Semántica 1 (Avance 3 - Errores Semánticos)
 * ===================================================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Pablo Naranjo (@PabloNaranjoM)
 *
 * Descripción:
 * Casos de prueba con errores semánticos deliberados enfocados en RS-2
 * (unicidad de identificadores en el alcance) y RS-5 (retorno de funciones,
 * parámetros variádicos y validación de argumentos en llamadas).
 */

import "fmt"

// [Error RS-2 #1]: Campo duplicado dentro de la misma estructura.
type Registro struct {
	codigo int
	codigo string
}

// Definición válida seguida de redeclaración de struct
type Curso struct {
	nombre string
}

// [Error RS-2 #2]: Redeclaración de struct en el ámbito global.
type Curso struct {
	creditos int
}

// [Error RS-2 #3]: Parámetro duplicado en la misma firma de función.
func conParametroRepetido(valor int, valor string) int {
	return valor
}

// [Error RS-5 #4]: Función tipada que retorna un tipo incompatible ('string' vs 'int').
func retornoIncompatible() int {
	return "no_soy_entero"
}

// [Error RS-5 #5]: Función tipada con sentencia 'return' vacía.
func retornoVacioEnTipada(activo bool) string {
	if activo {
		return
	}
	return "ok"
}

// [Error RS-5 #6]: Función con tipo de retorno declarado que omite la sentencia 'return'.
func faltaRetorno(x float64) float64 {
	calculo := x * 2.0
	fmt.Println(calculo)
}

// [Error RS-5 #7]: Función void que intenta retornar un valor.
func voidConRetorno() {
	return 42
}

// Función variádica válida para probar errores en llamadas
func sumarVariadico(base int, extras ...int) int {
	total := base
	for idx, v := range extras {
		if idx >= 0 {
			total += v
		}
	}
	return total
}

func duplicada() {
	fmt.Println("Primera definición")
}

// [Error RS-2 #8]: Redeclaración de función en el ámbito global.
func duplicada() {
	fmt.Println("Segunda definición")
}

func main() {
	// [Error RS-2 #9]: Redeclaración de variable en el mismo bloque.
	edad := 20
	var edad int = 25

	// [Error RS-2 #10]: Redeclaración con inferencia sobre identificador ya existente.
	var total = 10
	const total = 30

	// [Error RS-5 #11]: Llamada con cantidad de argumentos menor a la requerida.
	a := sumarVariadico()

	// [Error RS-5 #12]: Llamada variádica con argumento de tipo incompatible.
	b := sumarVariadico(10, "veinte")

	// [Error RS-5 #13]: Llamada a función normal con aridad incorrecta.
	c := conParametroRepetido(1)

	// [Error RS-5 #14]: Llamada a función normal con tipo de argumento inválido.
	d := faltaRetorno("texto")

	// [Error RS-5 / RS-1 #15]: Invocar una función no declarada.
	e := funcionInexistente(5)

	// [Error RS-5 #16]: Usar el retorno 'void' de una función como argumento.
	fmt.Println(voidConRetorno())

	// Uso de variables válidas restantes
	fmt.Println(edad, total)
}
