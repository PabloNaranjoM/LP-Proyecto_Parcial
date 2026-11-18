package main

/*
 * Algoritmo de Validación Semántica 2 (Avance 3 - Errores Semánticos)
 * ===================================================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Hivor Araujo (@AraujoHivor)
 *
 * Descripción:
 * Caso de prueba semántica con errores deliberados enfocados en RS-1
 * (declaración previa) y RS-3 (compatibilidad de asignaciones).
 */

 import "fmt"

type Persona struct {
    nombre string
    edad int
}

func main() {
    var edad int = 20
    const limite int = 100
    numeros := [3]int{10, 20, 30}
    lista := []int{1, 2, 3}
    edades := map[string]int{"Ana": 20}
    persona := Persona{nombre: "Ana", edad: 20}

    // RS-3: Asignar string a una variable int
    edad = "veinte"

    // RS-3: Intentar modificar una constante
    limite = 200

    // RS-1: Utilizar una variable no declarada
    fantasma = 10

    // RS-1: Indice incorrecto en un arreglo
    numeros["uno"] = 99

    // RS-1: Campo inexistente en una estructura
    persona.altura = 175

    // RS-1: Clave incorrecta en un mapa
    edades[1] = 30

    // RS-3: Elementos incompatibles en un slice
    incorrectos := []int{10, "texto"}

    // RS-3: Tipo incorrecto en un campo del struct
    otraPersona := Persona{nombre: "Luis", edad: "veinte"}

    // RS-3: Intentar leer datos sobre una constante
    fmt.Scanln(&limite)
}
