package main

/*
 * Algoritmo de Validación 1 - Analizador Léxico (Avance 1)
 * =======================================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Pablo Naranjo (@PabloNaranjoM)
 *
 * Descripción del algoritmo:
 * Simulación de un sistema financiero y contable que administra transacciones,
 * cotizaciones de divisas y balances de cuentas bancarias.
 *
 * Componentes evaluados asignados a Pablo Naranjo:
 * 1. Palabras reservadas oficiales: 'struct' y 'map'
 * 2. Tipos de datos numéricos: 'int' y 'float64'
 * 3. Operador de declaración y asignación corta: ':='
 * 4. Operadores de asignación compuesta: '+=', '-=', '*=', '/=', '%='
 * 5. Operadores unarios de incremento y decremento: '++', '--'
 * 6. Operador de dirección de memoria / puntero: '&'
 * 7. Delimitadores específicos: ':' y ';'
 * 8. Literales de punto flotante: e.g., 0.125, 1500.75, 1.085
 * 9. Literales de cadena con secuencias de escape: \", \n, \t, \\
 * 10. Comentarios de línea única (//) y bloques multilínea
 * 11. Errores léxicos deliberados: '@', '$', '~', '#' para verificar t_error
 */

import "fmt"

// Definición de estructura contable con tipos int y float64 (Pablo Naranjo)
type Transaccion struct {
	idTransaccion int
	tasaInteres   float64
	montoBase     float64
	totalFinal    float64
}

// Estructura auxiliar para saldos
type CuentaBancaria struct {
	numeroCuenta int
	saldoActual  float64
}

func main() {
	// 1. Declaración y asignación corta (:=) con tipos int y float64
	intentosMaximos := 3;
	tasaAnual := 0.125
	saldoInicial := 1500.75

	// 2. Instanciación de estructura (struct) con delimitador ':'
	operacion := Transaccion{
		idTransaccion: 1001,
		tasaInteres:   tasaAnual,
		montoBase:     saldoInicial,
		totalFinal:    0.0,
	}

	// 3. Operador ampersand (&) para referencia de memoria / punteros
	ptrOperacion := &operacion;

	// 4. Asignaciones compuestas (+=, -=, *=, /=, %=)
	operacion.montoBase += 350.50
	operacion.montoBase -= 75.25
	operacion.tasaInteres *= 1.05
	operacion.totalFinal /= 2.0
	operacion.idTransaccion %= 100

	// 5. Operadores de incremento (++) y decremento (--)
	intentosMaximos++
	intentosMaximos--

	// 6. Colección de tipo mapa (map) asociando cadenas con float64
	cotizaciones := map[string]float64{
		"USD": 1.00,
		"EUR": 1.085,
		"GBP": 1.295,
	}

	// 7. Literales de cadena con secuencias de escape (\", \n, \t, \\)
	mensajeEstado := "Reporte: \"Cierre Diario\"\n\tEstado: Exitoso \\ Verificado\n"

	/*
	 * Bloque de liquidación final de balances
	 * Cálculo del cargo por servicio administrativo
	 */
	cargoServicio := 4.75;
	operacion.totalFinal = operacion.montoBase + (operacion.montoBase * operacion.tasaInteres) - cargoServicio;

	// =========================================================================
	// SECCIÓN DE ERRORES LÉXICOS INTENCIONALES
	// Caracteres ilegales deliberados para evidenciar la captura en t_error
	// =========================================================================
	valorInvalido@ := 250.00         // Error: carácter ilegal '@'
	fondoReserva$ := 890.50          // Error: carácter ilegal '$'
	tasaAjuste~ := 0.03              // Error: carácter ilegal '~'
	tokenInvalido# := 99             // Error: carácter ilegal '#'

	// Variables en uso para evitar advertencias de compilador Go
	_ = ptrOperacion
	_ = cotizaciones
	_ = mensajeEstado
}
