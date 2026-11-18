package main

/*
 * Algoritmo de Validación Semántica 3 (Avance 3 - Caso Válido)
 * ============================================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Josué Pacheco (@JosuePach3co)
 *
 * Descripción:
 * Programa válido en Go enfocado en validar RS-4 (coherencia en
 * operaciones permitidas) y RS-6 (estructuras de control e interrupciones).
 */
 
import "fmt"

const MAX_INTENTOS int = 5
const BONO_EXCELENCIA float64 = 1.25

// Función auxiliar que valida RS-4 (relacionales, lógicas, aritmética float64)
// y RS-6 (if / else if / else con condiciones booleanas y return tipado).
func calcularPuntajeFinal(promedio float64, asistencias int, tieneSancion bool) float64 {
	var penalizacion float64 = 0.75
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

// Función auxiliar que valida RS-6 (switch tipado con fallthrough válido y default).
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
	// --- 1. RS-4: Operaciones aritméticas (+, -, *, /, %), unarias y strings ---
	prefijo := "ESPOL"
	materia := "Lenguajes de Programacion"
	encabezado := prefijo + " - " + materia
	fmt.Println(encabezado)

	var base int = 24
	factor := 3
	descuentoEntero := -4
	totalPuntos := (base+factor)*2 + descuentoEntero - (base / 4)
	residuoGrupo := totalPuntos % 4

	precioUnitario := 18.50
	cantidad := 4.0
	impuesto := 2.25
	totalFactura := (precioUnitario * cantidad) + impuesto - (impuesto / 3.0)
	fmt.Println("Total puntos:", totalPuntos, "| Residuo:", residuoGrupo, "| Factura:", totalFactura)

	// --- 2. RS-4 (++/--) y RS-6 (for clásico con continue y break) ---
	intentos := 0
	cuposDisponibles := 10
	acumuladoValidaciones := 0

	for i := 0; i < 6; i++ {
		if i == 1 {
			continue
		}
		intentos++
		cuposDisponibles--
		acumuladoValidaciones = acumuladoValidaciones + (i * 2)
		if intentos == 4 {
			break
		}
	}

	// --- 3. RS-6: for condicional con expresión booleana compuesta ---
	ciclosExtra := 0
	for intentos < MAX_INTENTOS && ciclosExtra < 3 {
		intentos++
		ciclosExtra++
	}

	// --- 4. RS-6: for range con variables nombradas sobre slice y map ---
	calificaciones := []float64{8.8, 9.4, 7.2, 9.7}
	sumaNotas := 0.0

	for indice, nota := range calificaciones {
		if nota < 0.0 {
			continue
		}
		sumaNotas = sumaNotas + nota
		fmt.Println("Registro", indice, "-> Nota:", nota)
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
		totalCreditos = totalCreditos + creditos
		fmt.Println("Curso:", nombreCurso, "| Créditos:", creditos)
	}

	// --- 5. RS-6: switch con selector y switch sin selector (booleanos) ---
	descripcionNivel := clasificarNivel(1)
	fmt.Println("Clasificación:", descripcionNivel)

	promedioGeneral := sumaNotas / 4.0
	notaFinal := calcularPuntajeFinal(promedioGeneral, 95, false)

	switch {
	case notaFinal >= 9.0 && totalCreditos >= 10:
		fmt.Println("Resultado: Aprobado con Distinción ->", notaFinal)
	case notaFinal >= 7.0 || residuoGrupo == 0:
		fmt.Println("Resultado: Aprobado Regular ->", notaFinal)
	default:
		fmt.Println("Resultado: Requiere Mejora ->", notaFinal)
	}
}