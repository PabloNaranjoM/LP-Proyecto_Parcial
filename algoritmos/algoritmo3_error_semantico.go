package main

/*
 * Algoritmo de Validación Semántica 3 (Avance 3 - Errores Semánticos)
 * ===================================================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Josué Pacheco (@JosuePach3co)
 *
 * Descripción:
 * Plantilla base para el algoritmo de prueba semántica con errores
 * deliberados enfocados en operaciones permitidas y estructuras de control.
 */

func main() {
	// TODO (Josué Pacheco): Implementar casos con errores semánticos deliberados
	//       y comentados por línea para validar:
	//       - RS-4 (operaciones permitidas): suma/operación entre `int` y `float64`,
	//         operador módulo `%` sobre `float64`, operadores lógicos `&&`/`||`/`!`
	//         sobre operandos no booleanos, comparaciones entre tipos distintos e
	//         incremento/decremento `++`/`--` sobre `string` o `const`.
	//       - RS-6 (estructuras de control): condición no booleana en `if` o `for`,
	//         incompatibilidad de tipo entre tag de `switch` y su `case`, uso de
	//         `break` o `continue` fuera de ciclo/switch y `fallthrough` fuera de `switch`.
}
