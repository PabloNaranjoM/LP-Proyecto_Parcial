package main

/*
 * Algoritmo de Validación Semántica 2 (Avance 3 - Errores Semánticos)
 * ===================================================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Hivor Araujo (@AraujoHivor)
 *
 * Descripción:
 * Plantilla base para el algoritmo de prueba semántica con errores
 * deliberados enfocados en declaración previa y compatibilidad de asignaciones.
 */

func main() {
	// TODO (Hivor Araujo): Implementar casos con errores semánticos deliberados
	//       y comentados por línea para validar:
	//       - RS-1 (identificadores): uso de variables o funciones no declaradas,
	//         acceso a campo inexistente en `struct`, e indexación con índice
	//         no entero o incompatible con la clave del mapa.
	//       - RS-3 (asignación de tipo): incompatibilidad estricta de tipos
	//         (`int` vs `float64`, `string` vs `int`), intento de reasignación de
	//         constantes `const`, literales compuestos heterogéneos y lectura
	//         sobre constante o variable no declarada (`fmt.Scanln(&CONST)`).
}
