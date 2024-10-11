def get_tipo(tipo):
        if tipo in (0, 1, 2):
            return "Carta Simple"
        elif tipo in (3, 4):
            return "Carta Certificada"
        elif tipo in (5, 6):
            return "Carta Expresa"

        return "Tipo de carta desconocido"

def get_pago(pago):
        if pago == 1:
            return "Efectivo"
        elif pago == 2:
            return "Tarjeta de crédito"

        return "Forma de pago desconocida"

class Envio:
    def __init__(self, cp, direccion, tipo, pago):
        self.cp = cp
        self.direccion = direccion
        self.tipo = tipo
        self.pago = pago

    def __str__(self):
        envio = "Código Postal: " + self.cp
        envio += " - País: " + self.get_pais()
        envio += " - Dirección: " + self.direccion
        envio += " - Tipo de envio: " + get_tipo(self.tipo) + "(tipo {0})".format(self.tipo)
        envio += " - Forma de Pago: " + get_pago(self.pago)
        return envio

    def calcular_importe_final(self):
        destino = self.get_pais()
        cp, tipo, pago = self.cp, self.tipo, self.pago

        importes = (1100, 1800, 2450, 8300, 10900, 14300, 17900)
        monto = importes[tipo]

        if destino == 'Argentina':
            inicial = monto
        else:
            if destino == 'Bolivia' or destino == 'Paraguay' or (destino == 'Uruguay' and cp[0] == '1'):
                inicial = int(monto * 1.20)
            elif destino == 'Chile' or (destino == 'Uruguay' and cp[0] != '1'):
                inicial = int(monto * 1.25)
            elif destino == 'Brasil':
                if cp[0] == '8' or cp[0] == '9':
                    inicial = int(monto * 1.20)
                else:
                    if cp[0] == '0' or cp[0] == '1' or cp[0] == '2' or cp[0] == '3':
                        inicial = int(monto * 1.25)
                    else:
                        inicial = int(monto * 1.30)
            else:
                inicial = int(monto * 1.50)

        final = inicial

        if pago == 1:
            final = int(0.9 * inicial)

        return final

    def get_pais(self):
        cp = self.cp
        n = len(cp)
        if n < 4 or n > 9:
            return 'Otro'

        if n == 8:
            if cp[0].isalpha() and cp[0] not in 'IO' and cp[1:5].isdigit() and cp[5:8].isalpha():
                return 'Argentina'
            else:
                return 'Otro'

        if n == 9:
            if cp[0:5].isdigit() and cp[5] == '-' and cp[6:9].isdigit():
                return 'Brasil'
            else:
                return 'Otro'

        if cp.isdigit():
            if n == 4:
                return 'Bolivia'

            if n == 7:
                return 'Chile'

            if n == 6:
                return 'Paraguay'

            if n == 5:
                return 'Uruguay'

        return 'Otro'