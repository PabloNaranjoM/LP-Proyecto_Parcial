package main
import "fmt"

/*
 * Algoritmo de Validación Semántica 2 (Avance 3 - Caso Válido)
 * ============================================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Hivor Araujo (@AraujoHivor)
 *
 * Descripción:
 * Plantilla base para el algoritmo de prueba semántica válido 2.
 * No utilizar el identificador en blanco '_' (usar identificadores nombrados).
 */


type Persona struct {
    nombre string
    edad int
}

func main() {
    // Variables y constantes
    var edad int = 20
    const limite int = 100

    // Asignaciones correctas
    edad = 21
    edad += 2

    // Inferencia de tipos
    nombre := "Ana"
    var mensaje = nombre

    // Arreglo y slice
    numeros := [3]int{10, 20, 30}
    lista := []int{1, 2, 3}

    // Mapa con claves string y valores int
    edades := map[string]int{"Ana": 20, "Luis": 25}

    // Inicializacion de estructura
    persona := Persona{nombre: "Ana", edad: 20}

    // Referencias a variables, indices y campos
    fmt.Println(edad, limite, mensaje)
    fmt.Println(numeros[0], lista[1])
    fmt.Println(edades["Ana"])
    fmt.Println(persona.nombre, persona.edad)

    // Lectura sobre variable modificable
    fmt.Scanln(&edad)
}
