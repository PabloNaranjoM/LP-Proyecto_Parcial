package main

// Prueba con un simbolo que el analizador debe reportar como error lexico.
func main() {
    var edad int = 20
    var resultado int = edad @ 3
    _ = resultado
}
