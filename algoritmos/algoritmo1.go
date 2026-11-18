package main

/*
 * Algoritmo Completo 1 (Válido) - Avance Final
 * ============================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Pablo Naranjo (@PabloNaranjoM)
 *
 * Descripción:
 * Programa completo y válido dentro del subconjunto aprobado de Go que integra
 * los aportes léxicos, sintácticos y semánticos (RS-2 y RS-5) de Pablo Naranjo:
 * - Léxico: struct, map, int, float64, :=, +=/-=/*=//=/%=, ++/--, &, :, ;, ...,
 *   fmt.Scanln/Scan, literales float64 y string con escapes, comentarios // y /* * /.
 * - Sintáctico: declaración corta, expresiones con / y %, relacionales, for
 *   (condicional, clásico, range e infinito), map, struct, variádicas y llamadas.
 * - Semántico: unicidad en el alcance y shadowing válido (RS-2); firmas,
 *   pre-registro, retorno en todas las rutas, void, variádicas y literal de función (RS-5).
 */

import "fmt"

// Ámbito global único (RS-2)
const bonoBase int = 5

var etiquetaGlobal string = "ESPOL"

// Definición de estructuras con campos únicos (RS-2 / RS-5)
type Transaccion struct {
	idTransaccion int
	tasaInteres   float64
	montoBase     float64
	totalFinal    float64
}

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

// Función variádica con parámetros enteros y bucle for range (RS-5)
func acumularPuntos(base int, extras ...int) int {
	total := base
	for idx, valor := range extras {
		if idx >= 0 {
			total += valor
		}
	}
	return total
}

// Función tipada con retorno en todas las rutas de ejecución (RS-5)
func esAprobado(nota float64, limite float64) bool {
	if nota >= limite {
		return true
	}
	return false
}

func main() {
	// 1. Shadowing válido: variable local oculta a la global sin conflicto (RS-2)
	etiquetaGlobal := 2026
	intentosMaximos := 3;
	tasaAnual := 0.125
	saldoInicial := 1500.75

	// 2. Instanciación de struct y operador '&' sobre variable mutable
	operacion := Transaccion{
		idTransaccion: 1001,
		tasaInteres:   tasaAnual,
		montoBase:     saldoInicial,
		totalFinal:    0.0,
	}
	ptrOperacion := &operacion;

	alumno := Estudiante{
		nombre:    "Pablo",
		matricula: 202601,
		promedio:  9.15,
	}

	// 3. Entrada estándar por teclado (fmt.Scanln / fmt.Scan)
	fmt.Scanln(&alumno.nombre, &intentosMaximos)
	fmt.Scan(&operacion.idTransaccion)

	// 4. Asignaciones compuestas (+=, -=, *=, /=, %=) e incremento/decremento (++, --)
	operacion.montoBase += 350.50
	operacion.montoBase -= 75.25
	operacion.tasaInteres *= 1.05
	operacion.totalFinal /= 2.0
	operacion.idTransaccion %= 100

	intentosMaximos++
	intentosMaximos--

	// 5. Mapa asociativo (map) e iteración con for range
	cotizaciones := map[string]float64{
		"USD": 1.00,
		"EUR": 1.085,
		"GBP": 1.295,
	}
	sumaDivisas := 0.0
	for divisa, tasa := range cotizaciones {
		sumaDivisas += tasa
		fmt.Println("Divisa:", divisa, "-> Tasa:", tasa)
	}

	// 6. Expresiones con '/', '%', paréntesis, negación '!' y relacionales
	residuo := (intentosMaximos + 10) / 3 % 2
	bloqueado := false
	accesoValido := !bloqueado && operacion.idTransaccion >= 0

	// 7. Variantes de bucle for (condicional, clásico e infinito con break)
	contador := 0
	for contador < 3 {
		contador++
	}

	acumulado := 0
	for i := 0; i < 4; i++ {
		acumulado += i
	}

	for {
		if acumulado >= 0 {
			break
		}
	}

	// 8. Literal de función e invocaciones con aridad y tipos exactos (RS-5)
	duplicar := func(n int) int {
		return n * 2
	}

	registrarAviso(false)
	registrarAviso(accesoValido)

	puntosBase := duplicar(bonoBase)
	puntajeTotal := acumularPuntos(puntosBase, 10, 15, 20)
	aprobado := esAprobado(alumno.promedio, 7.0)
	resumen := construirResumen(alumno.nombre, puntajeTotal, aprobado)

	// 9. Shadowing válido dentro de bloques hijos if y for (RS-2)
	estado := "pendiente"
	if aprobado {
		estado := 100
		fmt.Println("Estado interno if:", estado)
	}
	for paso := 0; paso < 2; paso++ {
		estado := true
		fmt.Println("Iteración", paso, "-> activo:", estado)
	}

	// 10. Cadenas con secuencias de escape (\", \n, \t, \\)
	mensajeEstado := "Reporte: \"Cierre Diario\"\n\tEstado: Exitoso \\ Verificado\n"
	fmt.Println(ptrOperacion, cotizaciones["USD"], sumaDivisas, residuo, resumen, estado, mensajeEstado)
}

// Función declarada después de main() para comprobar el pre-registro de firmas (RS-5)
func construirResumen(nombre string, puntos int, aprobado bool) string {
	if aprobado {
		return nombre + " aprobado"
	}
	return nombre + " reprobado"
}
