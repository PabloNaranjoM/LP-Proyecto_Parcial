package main

/*
 * Algoritmo de Validación 3 - Analizador Léxico (Avance 1)
 * =======================================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Josué Pacheco (@JosuePach3co)
 *
 * Descripción del algoritmo:
 * Simulación de un sistema de control de acceso y monitoreo de
 * seguridad que evalúa permisos y estados lógicos de sensores.
 *
 * Componentes evaluados asignados a Josué Pacheco:
 * 1. Tipo de dato predefinido: 'bool'
 * 2. Literales booleanos (constantes predefinidas): 'true' y 'false'
 * 3. Operadores relacionales: '==', '!=', '<', '>', '<=', '>='
 * 4. Operadores lógicos lógicos: '&&', '||', '!'
 * 5. Delimitadores específicos: ',' y '.'
 * 6. Errores léxicos deliberados: '@', '$', '~', '#' para verificar t_error
 */

import "fmt"

func main() {
	// 1. Tipo de dato predefinido 'bool' y literales 'true', 'false'
	var sistemaActivo bool = true
	var alertaIntrusion bool = false

	// Variables numéricas base para comprobaciones relacionales
	var nivelSeguridad int = 85
	var umbralMinimo int = 70

	// 2. Operadores relacionales (<, >, <=, >=, ==, !=)
	var requiereRevision bool = nivelSeguridad < 50
	var nivelMaximo bool = nivelSeguridad > 95
	var estadoCritico bool = nivelSeguridad <= 20
	var accesoPermitido bool = nivelSeguridad >= umbralMinimo
	var codigosCoinciden bool = nivelSeguridad == 85
	var fallaSensor bool = nivelSeguridad != 85

	// 3. Operadores lógicos (&&, ||, !)
	var activarAlarma bool = alertaIntrusion || !sistemaActivo
	var monitoreoEstable bool = sistemaActivo && accesoPermitido
	
	if (activarAlarma == true && monitoreoEstable != true) || !accesoPermitido {
		alertaIntrusion = true
	}

	// 4. Delimitadores específicos: punto (.) en llamadas y coma (,) en argumentos
	fmt.Println("Estado del sistema de acceso:", accesoPermitido, activarAlarma)
	
	//Sección de errores léxicos intencionales
	// Caracteres ilegales deliberados para evidenciar la captura en t_error
	
	var errorAcceso@ bool = false          // Error: carácter ilegal '@'
	var sensorFallo$ bool = true           // Error: carácter ilegal '$'
	var umbral~ int = 100                  // Error: carácter ilegal '~'
	var tokenRoto# bool = false            // Error: carácter ilegal '#'
	
	// Variables en uso para evitar advertencias de compilador Go
	_ = requiereRevision
	_ = nivelMaximo
	_ = estadoCritico
	_ = codigosCoinciden
	_ = fallaSensor
}
