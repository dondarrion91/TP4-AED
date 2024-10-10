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
        envio += " - Tipo de envio: " + self.get_tipo()
        envio += " - Forma de Pago: " + self.get_pago()
        return envio

    def get_pago(self):
        if self.pago == 1:
            return "Efectivo"
        elif self.pago == 2:
            return "Tarjeta de crédito"

        return "Forma de pago desconocida"

    def get_tipo(self):
        if self.tipo in (0, 1, 2):
            return "Carta Simple"
        elif self.tipo in (3, 4):
            return "Carta Certificada"
        elif self.tipo in (5, 6):
            return "Carta Expresa"

        return "Tipo de carta desconocido"

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