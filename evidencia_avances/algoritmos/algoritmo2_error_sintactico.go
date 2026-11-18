package main

/*
 * Algoritmo de Validación Sintáctica 2 (Avance 2 - Errores Sintácticos)
 * =====================================================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Hivor Araujo (@AraujoHivor)
 */

import "fmt"

func main() {
    // Instrucciones correctas para dar contexto a la prueba.
    var edad int = 25
    notas := [3]int{10, 9, 8}
    fmt.Println("Edad:", edad, "Primera nota:", notas[0])

    // Error sintactico 1: falta la expresion despues del signo igual.
    var limite int = ;

    // Error sintactico 2: falta cerrar el corchete del arreglo.
    var edades [3 int;

    // Error sintactico 3: hay dos operadores seguidos, sin operando.
    var suma int = edad + * 5;

    // Error sintactico 4: la condicion del if termina en &&.
    if edad >= 18 && {
        fmt.Println("Mayor de edad")
    }

    // Error sintactico 5: coma final sin otro argumento en Println.
    fmt.Println("Hola",)

    // Error sintactico 6: asignacion sin valor a la derecha.
    edad = ;

    // Error sintactico 7: falta un bloque entre llaves en el if.
    if edad >= 18 fmt.Println("Adulto")

    // Error sintactico 8: falta la coma entre dos argumentos.
    fmt.Println("Notas:" notas[0])
}
