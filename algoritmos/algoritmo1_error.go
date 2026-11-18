package main

/*
 * Algoritmo Completo 1 con Errores - Avance Final
 * ===============================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Pablo Naranjo (@PabloNaranjoM)
 *
 * Descripción:
 * Reúne en un solo archivo errores léxicos, sintácticos y semánticos (RS-2 y RS-5)
 * diseñados de modo que las tres fases se reporten en una misma ejecución sin
 * que los errores sintácticos impidan construir el AST.
 */

import "fmt"

// [Error Semántico RS-2]: Campo duplicado dentro de la misma estructura.
type Registro struct {
	codigo int
	codigo string
}

type Curso struct {
	nombre string
}

// [Error Semántico RS-2]: Redeclaración de struct en el ámbito global.
type Curso struct {
	creditos int
}

// [Error Semántico RS-2]: Parámetro duplicado en la misma firma de función.
func conParametroRepetido(valor int, valor string) int {
	return valor
}

// [Error Semántico RS-5]: Función tipada que retorna un tipo incompatible ('string' vs 'int').
func retornoIncompatible() int {
	return "no_soy_entero"
}

// [Error Semántico RS-5]: Función tipada con sentencia 'return' vacía.
func retornoVacioEnTipada(activo bool) string {
	if activo {
		return
	}
	return "ok"
}

// [Error Semántico RS-5]: Función tipada que omite la sentencia 'return'.
func faltaRetorno(x float64) float64 {
	calculo := x * 2.0
	fmt.Println(calculo)
}

// [Error Semántico RS-5]: Función tipada donde falta retorno en la rama 'else'.
func retornoIncompleto(x int) int {
	if x > 0 {
		return 1
	}
}

// [Error Semántico RS-5]: Función void que intenta retornar un valor.
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

// [Error Semántico RS-2]: Redeclaración de función en el ámbito global.
func duplicada() {
	fmt.Println("Segunda definición")
}

func main() {
	const bonoFijo int = 5
	edad := 20
	fmt.Scanln(&edad)

	// =========================================================================
	// 1. ERRORES LÉXICOS DELIBERADOS (@, $, ~, #)
	// =========================================================================
	valorInvalido@ := 250.00
	fondoReserva$ := 890.50
	tasaAjuste~ := 0.03
	tokenInvalido# := 99

	// =========================================================================
	// 2. ERRORES SINTÁCTICOS RECUPERABLES (sin desbalancear llaves)
	// =========================================================================
	tasa := ;
	residuo := (edad / 2 % 3;
	esMayor := edad >= ;

	// =========================================================================
	// 3. ERRORES SEMÁNTICOS (RS-2 y RS-5)
	// =========================================================================
	// [Error RS-2]: Redeclaración de variable en el mismo bloque.
	var edad int = 25

	// [Error RS-2]: Redeclaración con inferencia sobre identificador ya existente.
	var total = 10
	const total = 30

	// [Error RS-5]: Llamada variádica con cantidad de argumentos menor a la requerida.
	a := sumarVariadico()

	// [Error RS-5]: Llamada variádica con argumento de tipo incompatible.
	b := sumarVariadico(10, "veinte")

	// [Error RS-5]: Llamada a función normal con aridad incorrecta.
	c := conParametroRepetido(1)

	// [Error RS-5]: Llamada a función normal con tipo de argumento inválido.
	d := faltaRetorno("texto")

	// [Error RS-5 / RS-1]: Invocar una función no declarada.
	e := funcionInexistente(5)

	// [Error RS-5]: Usar el retorno 'void' de una función como argumento.
	fmt.Println(voidConRetorno())

	// [Error asignación de tipo]: Obtener dirección '&' de una constante.
	ptrBono := &bonoFijo

	fmt.Println(valorInvalido, fondoReserva, tasaAjuste, tokenInvalido, total)
}
