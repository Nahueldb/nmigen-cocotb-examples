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
