package main
import "fmt"

// Prueba de errores lexicos del analizador hecho con PLY.
// Tiene varias instrucciones normales y 5 caracteres invalidos a proposito.
func calcularTotal(precio int, cantidad int) int {
    subtotal := precio * cantidad
    if subtotal > 50 {
        subtotal = subtotal - 5
    } else {
        subtotal = subtotal + 2
    }
    return subtotal
}

func main() {
    var nombre string = "Ana"
    var precio@ int = 12             // Error 1: @ en el nombre de una variable
    var cantidad int = 4
    var descuento$ int = 3           // Error 2: $ en el nombre de una variable

    valores := [3]int{10, 20, 30}
    total := calcularTotal(precio, cantidad)
    total = total + valores[0] % 7

    for i := 0; i < 3; i++ {
        total = total + valores[i] / 2
    }

    total = total ? descuento        // Error 3: ? como operador no reconocido
    total = total # 2                // Error 4: # como operador no reconocido

    if total > 20 {
        fmt.Println(nombre, total)
    } else {
        fmt.Println("Sin cambios")
    }

    switch total {
    case 10:
        fmt.Println("Diez")
    default:
        fmt.Println("Otro valor")
    }

    var codigo@ int = 7             // Error 5: otro @ en identificador
    _ = codigo
}
