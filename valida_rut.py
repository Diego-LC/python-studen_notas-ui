import inicio
from itertools import cycle

def validarRut(rut):
    rut = rut.upper()
    rut = rut.replace("-","")
    rut = rut.replace(".","")
    aux = rut[:-1]
    dv = rut[-1:]

    revertido = map(int, reversed(str(aux)))
    factors = cycle(range(2,8))
#    print('rev',revertido)
    s = sum(d * f for d, f in zip(revertido,factors))
    res = (-s)%11

    if str(res) == dv:
        return True
    elif dv=="K" and res==10:
        return True
    else:
        return False

def boton_presionado(event=None):
    valor=entry.get()
    if (validarRut(str(valor))):
        print("Valido")
    else:
        print("No Valido")
