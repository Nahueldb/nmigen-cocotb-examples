# nmigen-cocotb-examples
## Adder

Sumador con lógica de números signados complemento a 2 que cumple con la siguiente
interfaz:

```
           |--------------|
 a_data -->|              |
a_valid -->|              |
a_ready <--|              |
           |              |-->  r_data
           |    Adder     |--> r_valid
           |              |<--  r_ready
 b_data -->|              |
b_valid -->|              |
b_ready <--|              |
           |--------------|
               ^       ^
               |       |
              rst     clk
```

Tanto las dos entradas como la salida cumplen un protocolo genérico stream con las
siguientes características:

* Las señales `_data` tienen N bits definidas durante la instanciación.
* La cantidad de bits de `r_data` quedan a definir por el diseñador. Algunas posibles alternativas son:
    * A definir durante la instanciación
    * Igual que la entrada
    * Un bit mas que la entrada 
* El dato `_data` es leído por el sumidero cuando `_valid` y `_ready` están en 1
* La señal `_valid` no puede depender depender de la señal `_ready` para ir a 1.

Todas los datos que salgan por el puerto `r` deben ser un resultado valido entre los datos
del puerto `a` y puerto `b`. No se debe realizar corroboración de overflow.
