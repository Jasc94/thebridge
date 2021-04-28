# --------------------- Clase Humano ---------------------
class Humano:

    def __init__(self, nombre, armadura, nivel, ataque, ojos = 2, piernas = 2, dientes = 32, salud = 100):
        self.nombre = nombre
        self.armadura = armadura
        self.nivel = nivel
        self.ataque = ataque
        self.ojos = ojos
        self.piernas = piernas
        self.dientes = dientes
        self.salud = salud

    def atacar(self, Orco):
        Orco.salud += Orco.armadura - self.ataque
        return Orco.salud

    def no_vivo(self):
        if self.salud < 0:
            return True

        else:
            return False

    def atributos(self):
        return 'Nombre: {} | Armadura: {} | Nivel: {} | Ataque: {} | Ojos: {} | Piernas: {} | Dientes: {} | Salud: {}'.format(
            self.nombre, self.armadura, self.nivel, self.ataque, self.ojos, self.piernas, self.dientes, self.salud
        )


# --------------------- Clase Orco ---------------------
class Orco:

    def __init__(self, nombre, armadura, nivel, ataque, ojos = 2, piernas = 2, dientes = 56, salud = 100):
        self.nombre = nombre
        self.armadura = armadura
        self.nivel = nivel
        self.ataque = ataque
        self.ojos = ojos
        self.piernas = piernas
        self.dientes = dientes
        self.salud = salud

    def atacar(self, Humano):
        Humano.salud += Humano.armadura - self.ataque
        return Humano.salud

    def no_vivo(self):
        if self.salud < 0:
            return True

        else:
            return False

    def atributos(self):
        return 'Nombre: {} | Armadura: {} | Nivel: {} | Ataque: {} | Ojos: {} | Piernas: {} | Dientes: {} | Salud: {}'.format(
            self.nombre, self.armadura, self.nivel, self.ataque, self.ojos, self.piernas, self.dientes, self.salud
        )


# --------------------- Testing ---------------------
#humano1 = Humano('humano1', 20, 5, 15)
#orco1 = Orco('orco1', 10, 7, 30)

#print('\nSituación inicial:\n')
#print(humano1.atributos(), '\n')
#print(orco1.atributos(), '\n')
#print('-' * 15, '\n')

#print('\nFirst round:\n')
#print('Vida restante del orco después del ataque humano:', humano1.atacar(orco1))
#print(orco1.salud)
#print('Vida restante del humano después del ataque orco:', orco1.atacar(humano1))
#print(humano1.salud)