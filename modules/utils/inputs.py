def input_int(msg, minv=None):
    while True:
        try:
            n = int(input(msg).strip())
            if minv is not None and n < minv:
                raise ValueError
            return n
        except ValueError:
            print("→ Número inválido.")

def input_float(msg, minv=None):
    while True:
        try:
            x = float(input(msg).strip().replace(",", "."))
            if minv is not None and x < minv:
                raise ValueError
            return x
        except ValueError:
            print("→ Importe inválido.")