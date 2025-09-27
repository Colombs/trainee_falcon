# %%
# ------------------------- AMBIENTE -------------------------
from rocketpy import Environment

# Configura as condições do local e data de lançamento
env = Environment(
    latitude=...,              # Descrição: Latitude do lançamento. (Responsável: Geral)
    longitude=...,             # Descrição: Longitude do lançamento. (Responsável: Geral)
    elevation=...,             # Descrição: Altitude do local de lançamento. (Responsável: Geral)
)

# Define a data e hora do lançamento
# Exemplo: env.set_date((2025, 10, 20, 14)) # Ano, Mês, Dia, Hora (UTC)
env.set_date(...)              # Descrição: Data e hora da simulação/lançamento. (Responsável: Geral)

# Define o modelo atmosférico
# Exemplo: env.set_atmospheric_model(type="StandardAtmosphere", file="standard_atmosphere.nc")
env.set_atmospheric_model(...) # Descrição: Modelo atmosférico para vento, pressão, etc. (Responsável: Setor de Aviônica)

# %%
# ------------------------- MOTOR -------------------------
from rocketpy import SolidMotor

motor = SolidMotor(
    thrust_source=...,         # Descrição: Arquivo de curva de empuxo do motor. (Responsável: Setor de Motor)
    dry_mass=...,908g              # Descrição: Massa do motor sem propelente. (Responsável: Setor de Motor)
    dry_inertia=...,           # Descrição: Inércia do motor sem propelente. (Tupla (Ixx, Iyy, Izz) em kg*m^2). (Responsável: Setor de Motor)
    nozzle_radius=..., 12,6mm  # Descrição: Raio do bocal do motor. (Responsável: Setor de Motor)
    throat_radius=..., 4,9mm  # Descrição: Raio do bocal do motor. (Responsável: Setor de Motor)
    grain_number=...,  3,75        # Descrição: Número de grãos de propelente. (Responsável: Setor de Motor)
    grain_density=...,         # Descrição: Densidade do propelente. (Responsável: Setor de Motor)
    grain_outer_radius=...,21mm    # Descrição: Raio externo do grão de propelente. (Responsável: Setor de Motor)
    grain_initial_inner_radius=...,8,9mm # Descrição: Raio interno inicial do grão. (Responsável: Setor de Motor)
    grain_initial_height=..., 80mm # Descrição: Altura inicial do grão. (Responsável: Setor de Motor)
    grain_separation=...,   0,5mm   # Descrição: Distância entre os grãos. (Responsável: Setor de Motor)
    grains_center_of_mass_position=..., # Descrição: Posição do centro de massa dos grãos. (Responsável: Setor de Motor)
    nozzle_position=...,   0    # Descrição: Posição do bocal em relação à ponta do motor. (Responsável: Setor de Motor)
    burn_time=...,             # Descrição: Tempo de queima do motor. (Responsável: Setor de Motor)
    coordinate_system_orientation="nozzle_to_combustion_chamber" # Orientação do sistema de coordenadas do motor
)

# %%
# ------------------------- FOGUETE -------------------------
from rocketpy import Rocket, NoseCone, Fins, Parachute

# Cria o objeto Foguete
falcon6 = Rocket(
    radius=...,                # Descrição: Raio externo do foguete. (Responsável: Estruturas e Aerodinâmica)
    mass=...,                  # Descrição: Massa total do foguete sem motor. (Responsável: Estruturas e Aerodinâmica)
    inertia=...,               # Descrição: Momentos de inércia do foguete. (Tupla (Ixx, Iyy, Izz) em kg*m^2). (Responsável: Estruturas e Aerodinâmica)
    power_off_drag=...,        # Descrição: Curva de arrasto com motor desligado. (Arquivo .csv). (Responsável: Estruturas e Aerodinâmica)
    power_on_drag=...,         # Descrição: Curva de arrasto com motor ligado. (Arquivo .csv). (Responsável: Estruturas e Aerodinâmica)
    center_of_mass_without_motor=..., # Descrição: Centro de massa do foguete sem o motor. (Responsável: Estruturas e Aerodinâmica)
    center_of_dry_mass=...     # Descrição: Centro de massa do foguete vazio. (Responsável: Estruturas e Aerodinâmica)
)

# Adiciona o motor ao foguete
falcon6.add_motor(motor, position=...) # A posição é medida a partir da ponta do foguete

# Define a rugosidade da superfície
falcon6.set_surface_roughness(...) # Descrição: Rugosidade da superfície externa. (Responsável: Estruturas e Aerodinâmica)

# Adiciona a Ogiva (Nose Cone)
nose = NoseCone(
    length=...,                # Descrição: Comprimento do nariz do foguete. (Responsável: Estruturas e Aerodinâmica)
    kind="..."                 # Tipo de ogiva (ex: 'ogive', 'conical', 'vonKarman')
    # Outros parâmetros como 'base_radius' podem ser necessários
)
falcon6.add_nose(nose, position=...) # Posição da ponta da ogiva

# Adiciona as Aletas (Fins)
# Exemplo: Fins(n=4, root_chord=0.12, tip_chord=0.06, span=0.1)
fins = Fins(...)               # Descrição: Número, tamanho e geometria das aletas. (Responsável: Estruturas e Aerodinâmica)
falcon6.add_fins(fins, position=...) # Posição do início das aletas

# Adiciona o sistema de recuperação (Paraquedas)
# Este processo pode ser dividido em drogue e principal, se necessário.
main_parachute = Parachute(
    name="main",
    cd_s=...,                   # Coeficiente de arrasto x área do paraquedas
    trigger="apogee",           # Gatilho para acionamento (ex: apogeu)
    # Adicione outros parâmetros conforme necessário (ex: lag, noise)
    # Descrição: Sistema de recuperação (paraquedas). (Responsável: Setor de Recuperação)
)
falcon6.add_parachute(main_parachute)

# %%
# ------------------------- VOO (SIMULAÇÃO) -------------------------
from rocketpy import Flight

# Configura os parâmetros do voo
flight = Flight(
    rocket=falcon6,            # Descrição: Referência ao foguete usado. (Responsável: Geral)
    environment=env,           # Descrição: Referência ao ambiente definido. (Responsável: Geral)
    rail_length=...,           # Descrição: Comprimento da torre/trilho de lançamento. (Responsável: Estruturas e Aerodinâmica)
    inclination=...,           # Descrição: Ângulo de inclinação do lançamento. (Responsável: Geral)
    heading=...                # Descrição: Direção do lançamento (Azimute, 0-360). (Responsável: Geral)
)