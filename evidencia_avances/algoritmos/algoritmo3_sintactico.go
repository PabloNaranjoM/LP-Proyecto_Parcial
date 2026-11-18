package main

/*
 * Algoritmo de Validación Sintáctica 3 (Avance 2 - Caso Válido)
 * =============================================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Josué Pacheco (@JosuePach3co)
 */

import "fmt"

func main() {
	var promedio = 9.45
	var intentos = 10
	var autorizado = false

	restante := intentos - 3
	permitido := autorizado || promedio >= 9.0

	notas := []float64{8.5, 9.0, 10.0}

	duplicar := func(n int) int {
		return n * 2
	}

	intentos = duplicar(restante)
	intentos += 4
	intentos -= 1
	intentos++
	intentos--

	switch intentos {
	case 1:
		fmt.Print("Un intento registrado")
		break
	case 2:
		fmt.Print("Dos intentos registrados")
	default:
		fmt.Print("Múltiples intentos: ", intentos, notas[0], permitido)
	}
}
