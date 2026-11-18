package main

/*
 * Algoritmo Completo 3 (Válido) - Avance Final
 * ============================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Josué Pacheco (@JosuePach3co)
 *
 * Descripción:
 * Programa completo y válido en Go que integra los aportes léxicos,
 * sintácticos y semánticos (RS-4 y RS-6) de Josué Pacheco:
 * - Léxico: bool, true, false, Print, relacionales (==, !=, <, >, <=, >=),
 *   lógicos (&&, ||, !), coma (,) y punto (.).
 * - Sintáctico: bloques, var con inferencia, literal de función, slices,
 *   switch/case/default (con y sin selector), break/continue/fallthrough, fmt.Print,
 *   asignaciones compuestas, ++/-- y resta.
 * - Semántico: coherencia estricta en operaciones (RS-4) y validez lógica de
 *   estructuras de control e interrupciones (RS-6).
 */

import "fmt"

const MAX_INTENTOS int = 5
const BONO_EXCELENCIA float64 = 1.25

// Valida RS-4 (relacionales, lógicas, unario '-') y RS-6 (if / else if / else)
func calcularPuntajeFinal(promedio float64, asistencias int, tieneSancion bool) float64 {
	var penalizacion = 0.75
	ajusteNegativo := -penalizacion

	esCandidatoBeca := (promedio >= 8.5 && asistencias >= 90) || (!tieneSancion && promedio > 8.0)
	if esCandidatoBeca {
		return promedio + BONO_EXCELENCIA
	} else if promedio >= 7.0 && !tieneSancion {
		return promedio
	} else {
		return promedio + ajusteNegativo
	}
}

// Valida RS-6 (switch con selector, fallthrough válido y default)
func clasificarNivel(codigoNivel int) string {
	var etiqueta string = "Sin clasificar"
	switch codigoNivel {
	case 1:
		etiqueta = "Nivel Inicial"
		fallthrough
	case 2:
		etiqueta = "Nivel Intermedio Validado"
	case 3:
		etiqueta = "Nivel Avanzado"
	default:
		etiqueta = "Nivel Extraordinario"
	}
	return etiqueta
}

func main() {
	// 1. Inferencia con var, booleanos, relacionales y lógicos (RS-4)
	var promedio = 9.45
	var activo bool = true
	var alerta bool = false

	prefijo := "ESPOL"
	materia := "Lenguajes de Programacion"
	encabezado := prefijo + " - " + materia
	fmt.Println(encabezado)

	// 2. Expresiones aritméticas (+, -, *, /, %), unario '-' y literal de función
	var base int = 24
	factor := 3
	descuentoEntero := -4
	totalPuntos := (base+factor)*2 + descuentoEntero - (base / 4)
	residuoGrupo := totalPuntos % 4

	duplicar := func(n int) int {
		return n * 2
	}
	puntosDoble := duplicar(totalPuntos)

	// 3. Asignaciones compuestas, ++/-- y ciclo for clásico con continue y break (RS-6)
	intentos := 0
	cuposDisponibles := 10
	acumulado := 0

	for i := 0; i < 6; i++ {
		if i == 1 {
			continue
		}
		intentos++
		cuposDisponibles--
		acumulado += i * 2
		if intentos == 4 {
			break
		}
	}
	acumulado -= 1

	// 4. For condicional con operadores lógicos
	ciclosExtra := 0
	for intentos < MAX_INTENTOS && ciclosExtra < 3 {
		intentos++
		ciclosExtra++
	}

	// 5. Slices, mapas y for range (RS-6)
	calificaciones := []float64{8.8, 9.4, 7.2, 9.7}
	sumaNotas := 0.0
	for indice, nota := range calificaciones {
		if nota < 0.0 {
			continue
		}
		sumaNotas += nota
		fmt.Print("Registro ", indice, " -> Nota: ", nota, "\n")
	}

	creditosPorCurso := map[string]int{
		"Compiladores": 4,
		"Sistemas":     4,
		"Algoritmos":   3,
	}
	totalCreditos := 0
	for nombreCurso, creditos := range creditosPorCurso {
		if creditos <= 0 {
			continue
		}
		totalCreditos += creditos
		fmt.Println("Curso:", nombreCurso, "| Créditos:", creditos)
	}

	// 6. Switch con selector y switch sin selector booleano (RS-6)
	descripcionNivel := clasificarNivel(1)
	promedioGeneral := sumaNotas / 4.0
	notaFinal := calcularPuntajeFinal(promedioGeneral, 95, false)
	permitido := (activo && !alerta) || (promedio >= 9.0 && totalCreditos != 0)

	switch {
	case notaFinal >= 9.0 && totalCreditos >= 10 && permitido:
		fmt.Print("Aprobado con Distinción: ", notaFinal, " | Nivel: ", descripcionNivel, " | Doble: ", puntosDoble)
	case notaFinal >= 7.0 || residuoGrupo == 0:
		fmt.Print("Aprobado Regular: ", notaFinal)
	default:
		fmt.Print("Requiere Mejora: ", notaFinal)
	}
}
