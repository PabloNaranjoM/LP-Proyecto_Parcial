package main

/*
 * Algoritmo de Validación Semántica 1 (Avance 3 - Caso Válido)
 * ============================================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Pablo Naranjo (@PabloNaranjoM)
 *
 * Descripción:
 * Programa válido en Go enfocado en validar RS-2 (unicidad en el alcance
 * y shadowing entre ámbitos) y RS-5 (definición de structs, funciones
 * tipadas, variádicas, funciones void con return vacío, literales
 * de función y llamadas válidas).
 */

import "fmt"

// Ámbito global único (RS-2)
const bonoBase int = 5

var etiquetaGlobal string = "ESPOL"

// Definición de struct con campos únicos (RS-2 / RS-5)
type Estudiante struct {
	nombre    string
	matricula int
	promedio  float64
}

// Función void con return vacío temprano (RS-5)
func registrarAviso(activo bool) {
	if !activo {
		return
	}
	fmt.Println("Aviso:", etiquetaGlobal)
}

// Función variádica con parámetros enteros (RS-5)
func acumularPuntos(base int, extras ...int) int {
	total := base
	for idx, valor := range extras {
		if idx >= 0 {
			total += valor
		}
	}
	return total
}

// Función con retorno bool que invoca a otra declarada más abajo (pre-registro RS-5)
func esAprobado(nota float64, limite float64) bool {
	if nota >= limite {
		return true
	}
	return false
}

func main() {
	// Shadowing válido: 'etiquetaGlobal' local oculta la global sin conflicto RS-2
	etiquetaGlobal := 2026
	fmt.Println("Periodo local:", etiquetaGlobal)

	// Instanciación de struct sin comillas en los nombres de campo
	alumno := Estudiante{
		nombre:    "Pablo",
		matricula: 202601,
		promedio:  9.15,
	}

	// Literal de función (ámbito propio y firma funcional)
	duplicar := func(n int) int {
		return n * 2
	}

	// Invocaciones con aridad y tipos exactos (RS-5)
	registrarAviso(false)
	registrarAviso(true)

	puntosBase := duplicar(bonoBase)
	puntajeTotal := acumularPuntos(puntosBase, 10, 15, 20)
	aprobado := esAprobado(alumno.promedio, 7.0)
	resumen := construirResumen(alumno.nombre, puntajeTotal, aprobado)

	// Shadowing válido dentro de bloque if y bloque for (RS-2)
	estado := "pendiente"
	if aprobado {
		estado := 100
		fmt.Println("Estado interno if:", estado)
	}
	for paso := 0; paso < 2; paso++ {
		estado := true
		fmt.Println("Iteración", paso, "-> activo:", estado)
	}

	fmt.Println(resumen, "-> estado externo:", estado)
}

// Función declarada después de main() para comprobar el pre-registro de firmas
func construirResumen(nombre string, puntos int, aprobado bool) string {
	if aprobado {
		return nombre + " aprobado"
	}
	return nombre + " reprobado"
}
