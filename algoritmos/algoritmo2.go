/*
 * Algoritmo de Validación 2 - Analizador Léxico (Avance 1)
 * =======================================================
 * Materia    : Lenguajes de Programación (ESPOL)
 * Docente    : Ing. Rodrigo Saraguro
 * Responsable: Hivor Araujo (@AraujoHivor)
 *
 */
package main
import "fmt"

// Prueba 2: uso de variables, operaciones, arreglos y estructuras de control.
func calcularTotal(precio int, cantidad int) int {
    total := precio * cantidad
    if total > 30 {
        total = total - 5
    } else {
        total = total + 2
    }
    return total
}

func main() {
    var nombre string = "Ana"
    var variable int = 2
    numeros := [3]int{10, 20, 30}
    resultado := calcularTotal(numeros[0], 4)

    for i := 0; i < 3; i++ {
        if i == 1 {
            continue
        }
        resultado = resultado + numeros[i] % 7
    }

    mitad := resultado / 2
    resultado = mitad + variable * 3 - 1

    switch resultado {
    case 10:
        fmt.Println("El resultado es diez")
    default:
        fmt.Println(nombre, resultado)
    }
}
