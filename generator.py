import pandas as pd
import random
from datetime import datetime, timedelta
from faker import Faker

# ==========================================
# CONFIGURACIÓN INICIAL
# ==========================================
fake = Faker('es_MX')

aeropuertos_globales = {
    'CJS': {'nombre': 'Ciudad Juárez, MX', 'utc': -7},
    'ELP': {'nombre': 'El Paso, USA', 'utc': -7},
    'NLU': {'nombre': 'Ciudad México (AIFA), MX', 'utc': -6},
    'MEX': {'nombre': 'Ciudad México (AICM), MX', 'utc': -6},
    'GDL': {'nombre': 'Guadalajara, MX', 'utc': -6},
    'MTY': {'nombre': 'Monterrey, MX', 'utc': -6},
    'OAX': {'nombre': 'Oaxaca, MX', 'utc': -6},
    'CUN': {'nombre': 'Cancún / Riviera Maya, MX', 'utc': -5},
    'CZM': {'nombre': 'Cancún / Riviera Maya, MX', 'utc': -5},
    'TQO': {'nombre': 'Cancún / Riviera Maya, MX', 'utc': -5},
    'LAX': {'nombre': 'Los Ángeles, USA', 'utc': -8},
    'DFW': {'nombre': 'Dallas, USA', 'utc': -6},
    'IAH': {'nombre': 'Houston, USA', 'utc': -6},
    'JFK': {'nombre': 'Nueva York, USA', 'utc': -5},
    'ATL': {'nombre': 'Atlanta, USA', 'utc': -5},
    'ORD': {'nombre': 'Chicago, USA', 'utc': -6},
    'MAD': {'nombre': 'Madrid, España', 'utc': 1},
    'BCN': {'nombre': 'Barcelona, España', 'utc': 1},
    'CDG': {'nombre': 'París, Francia', 'utc': 1},
    'LHR': {'nombre': 'Londres, Reino Unido', 'utc': 0},
    'BER': {'nombre': 'Berlín, Alemania', 'utc': 1},
    'ZRH': {'nombre': 'Zúrich, Suiza', 'utc': 1},
    'AMS': {'nombre': 'Ámsterdam, Países Bajos', 'utc': 1},
    'FCO': {'nombre': 'Roma, Italia', 'utc': 1},
    'PEK': {'nombre': 'Pekín, China', 'utc': 8},
    'NRT': {'nombre': 'Tokio, Japón', 'utc': 9},
    'HND': {'nombre': 'Tokio, Japón', 'utc': 9},
    'ICN': {'nombre': 'Seúl, Corea del Sur', 'utc': 9},
    'BKK': {'nombre': 'Bangkok, Tailandia', 'utc': 7},
    'DPS': {'nombre': 'Bali, Indonesia', 'utc': 8}
}

aero_mx = ['NLU', 'MEX', 'GDL', 'MTY', 'OAX', 'CUN', 'CZM', 'TQO']
aero_usa = ['LAX', 'DFW', 'IAH', 'JFK', 'ATL', 'ORD']
aero_eu = ['MAD', 'BCN', 'CDG', 'LHR', 'BER', 'ZRH', 'AMS', 'FCO']
aero_as = ['PEK', 'NRT', 'HND', 'ICN', 'BKK', 'DPS']

# ==========================================
# MÓDULO 1: GENERACIÓN DE DIMENSIONES (CATÁLOGOS)
# ==========================================
print("Iniciando generación de Dimensiones (Catálogos Maestros)...")

# --- 1.1 DIM_AGENTES ---
def generar_agente(id_agente):
    return {
        'id_agente': id_agente,
        'nombre': fake.first_name(),
        'apellido': fake.last_name(),
        'edad': random.randint(18, 65),
        'email': fake.email(),
        'password': fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True),
        'fecha_registro': fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d')
    }
df_agentes = pd.DataFrame([generar_agente(i) for i in range(1000, 1010)])

# --- 1.2 DIM_CLIENTES ---
def generar_cliente(id_cliente):
    nacionalidad = random.choice(['Mexicano','Estadounidense'])
    telefono = ('656' if nacionalidad == 'Mexicano' else '915') + str(random.randint(1000000,9999999))
    return {
        'id_cliente': id_cliente,
        'nombre_titular': fake.name(),
        'edad': random.randint(18,65),
        'email': fake.email(),
        'telefono': telefono,
        'nacionalidad': nacionalidad
    }
df_clientes = pd.DataFrame([generar_cliente(i) for i in random.sample(range(10000,11000), 1000)])

# --- 1.3 DIM_VUELOS (RUTAS) ---
def generar_ruta_vuelo(id_vuelo):
    origen_iata = random.choice(['CJS', 'ELP'])
    numero_escalas = 0
    escala_1 = None
    escala_2 = None
    hora_salida_base = random.choice(['06:00', '08:30', '12:15', '17:45', '22:00'])
    
    if origen_iata == 'CJS':
        destino_iata = random.choice(aero_mx)
        aerolinea = random.choice(['Aeroméxico', 'Volaris', 'VivaAerobus'])
        asientos_eco, asientos_premium, asientos_vip = 75, 45, 30
        duracion_horas = round(random.uniform(1.5, 4.0), 1)
        numero_escalas = random.choice([0, 1])
        if numero_escalas == 1:
            escala_1 = 'MEX' if destino_iata != 'MEX' else 'MTY'
            duracion_horas += 1.5
    else: 
        destino_iata = random.choice(aero_usa + aero_eu + aero_as)
        aerolinea = random.choice(['American Airlines', 'Delta', 'United Airlines'])
        asientos_eco, asientos_premium, asientos_vip = 150, 90, 60
        if destino_iata in aero_usa:
            numero_escalas = 1
            escala_1 = random.choice([apt for apt in aero_usa if apt != destino_iata])
            duracion_horas = round(random.uniform(3.5, 7.0), 1)
        elif destino_iata in aero_eu:
            numero_escalas = random.choice([1, 2])
            escala_1 = random.choice(aero_usa)
            duracion_horas = round(random.uniform(11.0, 15.0), 1)
            if numero_escalas == 2:
                escala_2 = random.choice([apt for apt in aero_eu if apt != destino_iata])
                duracion_horas += 2.0
        elif destino_iata in aero_as:
            numero_escalas = random.choice([1, 2])
            escala_1 = random.choice(aero_usa)
            duracion_horas = round(random.uniform(16.0, 22.0), 1)
            if numero_escalas == 2:
                escala_2 = random.choice([apt for apt in aero_as if apt != destino_iata])
                duracion_horas += 2.5

    diferencia_horaria = aeropuertos_globales[destino_iata]['utc'] - aeropuertos_globales[origen_iata]['utc']

    return {
        'id_ruta': id_vuelo, 
        'aerolinea': aerolinea,
        'origen_iata': origen_iata,
        'origen': aeropuertos_globales[origen_iata]['nombre'],
        'destino_iata': destino_iata,
        'destino': aeropuertos_globales[destino_iata]['nombre'],
        'hora_salida_estandar': hora_salida_base,
        'duracion_estimada_horas': duracion_horas,
        'diferencia_horaria_destino': diferencia_horaria,
        'numero_escalas': numero_escalas,
        'escala_1': escala_1,
        'escala_2': escala_2,
        'stock_economica': asientos_eco,
        'stock_premium': asientos_premium,
        'stock_vip': asientos_vip
    }
df_catalogo_vuelos = pd.DataFrame([generar_ruta_vuelo(f"RUT-{i}") for i in range(1000, 1400)])

# --- 1.4 DIM_HOTELES ---
cadenas_hoteleras = {
    3: ['Holiday Inn', 'Ibis Styles', 'Best Western', 'City Express', 'Comfort Inn'],
    4: ['Marriott', 'Hilton', 'Sheraton', 'Hyatt Regency', 'Novotel'],
    5: ['Ritz-Carlton', 'Four Seasons', 'St. Regis', 'Waldorf Astoria', 'The Peninsula']
}
destinos_vuelos = [iata for iata in aero_mx + aero_usa + aero_eu + aero_as if iata not in ['CJS', 'ELP']]
lista_hoteles = []

for i in range(600):
    destino_iata = random.choice(destinos_vuelos)
    nombre_destino = aeropuertos_globales[destino_iata]['nombre']
    estrellas = random.choice([3, 4, 5])
    nombre_hotel = f"{random.choice(cadenas_hoteleras[estrellas])} {nombre_destino.split(',')[0]} {random.choice(['Centro', 'Airport', 'Resort & Spa', 'Financial District', 'Boutique'])}"
    
    multiplicador = 1.0 if destino_iata in aero_mx else (1.8 if destino_iata in aero_usa else 2.5)
    precio_base = (80 if estrellas == 3 else (150 if estrellas == 4 else 350)) * multiplicador
    
    lista_hoteles.append({
        'id_hotel': f"HTL-{1000 + i + 1}",
        'nombre_hotel': nombre_hotel,
        'destino_iata': destino_iata,
        'ciudad_destino': nombre_destino,
        'estrellas': estrellas,
        'precio_noche_estandar': round(precio_base, 2),
        'precio_noche_premium': round(precio_base * 1.4, 2),
        'precio_noche_vip': round(precio_base * 2.0, 2),
        'total_cuartos_estandar': 60,
        'total_cuartos_premium': 35,
        'total_cuartos_vip': 15
    })
df_catalogo_hoteles = pd.DataFrame(lista_hoteles)

# --- 1.5 DIM_TOURS ---
categorias_tour = ['Histórico', 'Natural', 'Diversión', 'Gastronómico', 'Aventura']
lista_tours = []
contador_tour = 1

for destino_iata in destinos_vuelos:
    nombre_destino = aeropuertos_globales[destino_iata]['nombre'].split(',')[0]
    multiplicador = 1.0 if destino_iata in aero_mx else (1.5 if destino_iata in aero_usa else 2.0)
        
    for categoria in categorias_tour:
        lista_tours.append({
            'id_tour': f"TOUR-{1000 + contador_tour}",
            'destino_iata': destino_iata,
            'ciudad_destino': nombre_destino,
            'categoria': categoria,
            'nombre_tour': f"Tour {categoria} en {nombre_destino}",
            'precio_por_persona': round(random.randint(30, 90) * multiplicador, 2),
            'capacidad_maxima': 30,
            'hora_inicio_fija': random.choice(['08:00', '10:00', '14:00', '16:00'])
        })
        contador_tour += 1
df_catalogo_tours = pd.DataFrame(lista_tours)

# --- 1.6 DIM_AUTOS ---
categorias_auto = {
    'Económico': {'pasajeros': 4, 'precio_base': 25},
    'Sedán': {'pasajeros': 5, 'precio_base': 40},
    'SUV': {'pasajeros': 5, 'precio_base': 65},
    'Premium': {'pasajeros': 5, 'precio_base': 110},
    'Van Familiar': {'pasajeros': 7, 'precio_base': 85}
}
lista_autos = []

for i in range(300):
    aeropuerto_iata = random.choice(list(aeropuertos_globales.keys()))
    categoria = random.choice(list(categorias_auto.keys()))
    transmision = 'Automático' if categoria != 'Económico' else random.choice(['Manual', 'Automático'])
    multiplicador = 1.0 if aeropuerto_iata in aero_mx else (1.6 if aeropuerto_iata in aero_usa else 2.1)
    
    lista_autos.append({
        'id_auto': f"AUT-{1000 + i + 1}",
        'categoria_auto': categoria,
        'arrendadora': random.choice(['Hertz', 'Avis', 'Enterprise', 'Budget', 'National']),
        'aeropuerto_ubicacion': aeropuerto_iata,
        'ciudad_ubicacion': aeropuertos_globales[aeropuerto_iata]['nombre'].split(',')[0],
        'capacidad_pasajeros': categorias_auto[categoria]['pasajeros'],
        'transmision': transmision,
        'tarifa_dia': round(categorias_auto[categoria]['precio_base'] * multiplicador, 2),
        'flota_total_modelo': random.randint(5, 12)
    })
df_catalogo_autos = pd.DataFrame(lista_autos)

# --- 1.7 DIM_TRASLADOS ---
tipos_servicio = {
    'Colectivo Económico': {'capacidad': 16, 'precio_base': 15, 'cobro': 'Por Persona'},
    'Colectivo Premium': {'capacidad': 16, 'precio_base': 25, 'cobro': 'Por Persona'},
    'Transporte Privado': {'capacidad': 4, 'precio_base': 80, 'cobro': 'Por Vehículo'}
}
lista_traslados = []
contador_traslado = 1

for _, hotel in df_catalogo_hoteles.iterrows():
    mult_region = 1.0 if hotel['destino_iata'] in aero_mx else (1.8 if hotel['destino_iata'] in aero_usa else 2.5)
    mult_estrellas = 1.0 if hotel['estrellas'] == 3 else (1.3 if hotel['estrellas'] == 4 else 1.7)
    
    for servicio, reglas in tipos_servicio.items():
        tarifa_sencilla = round(reglas['precio_base'] * mult_region * mult_estrellas, 2)
        lista_traslados.append({
            'id_traslado': f"TRN-{10000 + contador_traslado}",
            'id_hotel_destino': hotel['id_hotel'],
            'recogida_aeropuerto_iata': hotel['destino_iata'],
            'operadora': random.choice(['Global Transfers', 'QuickShuttle', 'Elite Ride']),
            'tipo_servicio': servicio,
            'capacidad_maxima': reglas['capacidad'],
            'tipo_cobro': reglas['cobro'],
            'tarifa_sencilla': tarifa_sencilla,
            'tarifa_redonda': round(tarifa_sencilla * 1.75, 2)
        })
        contador_traslado += 1
df_catalogo_traslados = pd.DataFrame(lista_traslados)

# --- 1.8 DIM_SEGUROS ---
tipos_cobertura = [
    {'tipo': 'Básica (Daños a Terceros)', 'cobertura': 15.00, 'silla': 10.00, 'conductor': 12.00},
    {'tipo': 'Amplia (Colisión y Robo)', 'cobertura': 30.00, 'silla': 10.00, 'conductor': 12.00},
    {'tipo': 'Premium (Cero Deducible)', 'cobertura': 55.00, 'silla': 0.00, 'conductor': 0.00}
]
df_catalogo_addons = pd.DataFrame([{
    'id_addon': f"ADD-{100 + i + 1}", 'tipo_cobertura': p['tipo'], 'costo_cobertura': p['cobertura'],
    'costo_silla_bebe': p['silla'], 'costo_conductor_extra': p['conductor']
} for i, p in enumerate(tipos_cobertura)])

print("Dimensiones procesadas correctamente.")

# ==========================================
# MÓDULO 2: GENERACIÓN DE INVENTARIOS (TIEMPO CONTINUO)
# ==========================================
print("Generando Inventarios Temporales (Big Data)...")

fecha_inicio = '2023-05-20'
fecha_fin = '2027-03-20'
calendario_dias = pd.date_range(start=fecha_inicio, end=fecha_fin, freq='D')

# --- 2.1 INV_VUELOS ---
inventario_itinerarios = []
contador_itinerario = 1
for _, ruta in df_catalogo_vuelos.iterrows():
    for dia in calendario_dias:
        hora_salida_str = f"{dia.strftime('%Y-%m-%d')} {ruta['hora_salida_estandar']}:00"
        fecha_hora_salida = datetime.strptime(hora_salida_str, '%Y-%m-%d %H:%M:%S')
        es_futuro = dia > datetime.now()
        
        inventario_itinerarios.append({
            'id_itinerario': f"ITN-{contador_itinerario}",
            'id_ruta': ruta['id_ruta'],
            'fecha_hora_salida': fecha_hora_salida,
            'asientos_disponibles_eco': ruta['stock_economica'] - (0 if es_futuro else random.randint(0, ruta['stock_economica'])),
            'asientos_disponibles_premium': ruta['stock_premium'] - (0 if es_futuro else random.randint(0, ruta['stock_premium'])),
            'asientos_disponibles_vip': ruta['stock_vip'] - (0 if es_futuro else random.randint(0, ruta['stock_vip']))
        })
        contador_itinerario += 1
df_itinerarios = pd.DataFrame(inventario_itinerarios)
df_itinerarios['fecha_busqueda'] = pd.to_datetime(df_itinerarios['fecha_hora_salida']).dt.date

# --- 2.2 INV_HOTELES ---
inventario_hoteles = []
contador_inv_hotel = 1
for _, hotel in df_catalogo_hoteles.iterrows():
    for dia in calendario_dias:
        pct = random.uniform(0.30, 0.90)
        inventario_hoteles.append({
            'id_inventario_hotel': f"INV-HTL-{contador_inv_hotel}",
            'id_hotel': hotel['id_hotel'],
            'fecha': dia.date(),
            'cuartos_disponibles_estandar': hotel['total_cuartos_estandar'] - int(hotel['total_cuartos_estandar'] * pct),
            'cuartos_disponibles_premium': hotel['total_cuartos_premium'] - int(hotel['total_cuartos_premium'] * pct),
            'cuartos_disponibles_vip': hotel['total_cuartos_vip'] - int(hotel['total_cuartos_vip'] * pct)
        })
        contador_inv_hotel += 1
df_inventario_hoteles = pd.DataFrame(inventario_hoteles)

# --- 2.3 INV_TOURS ---
inventario_tours = []
contador_inv_tour = 1
for _, tour in df_catalogo_tours.iterrows():
    for dia in calendario_dias:
        inventario_tours.append({
            'id_inventario_tour': f"INV-TR-{contador_inv_tour}",
            'id_tour': tour['id_tour'],
            'fecha': dia.date(),
            'hora_inicio': tour['hora_inicio_fija'],
            'lugares_disponibles': tour['capacidad_maxima'] - int(tour['capacidad_maxima'] * random.uniform(0.20, 0.85))
        })
        contador_inv_tour += 1
df_inventario_tours = pd.DataFrame(inventario_tours)

# --- 2.4 INV_AUTOS ---
inventario_autos = []
contador_inv_auto = 1
for _, auto in df_catalogo_autos.iterrows():
    for dia in calendario_dias:
        inventario_autos.append({
            'id_inventario_auto': f"INV-AUT-{contador_inv_auto}",
            'id_auto': auto['id_auto'],
            'fecha': dia.date(),
            'autos_disponibles': auto['flota_total_modelo'] - int(auto['flota_total_modelo'] * random.uniform(0.35, 0.90))
        })
        contador_inv_auto += 1
df_inventario_autos = pd.DataFrame(inventario_autos)

print("Inventarios procesados correctamente.")

# ==========================================
# MÓDULO 3: MOTOR TRANSACCIONAL CRM
# ==========================================
print("Indexando estructuras Hash en memoria...")
dict_idx_vuelos = {(r, f): i for i, r, f in zip(df_itinerarios.index, df_itinerarios['id_ruta'], df_itinerarios['fecha_busqueda'])}
dict_idx_hoteles = {(h, f): i for i, h, f in zip(df_inventario_hoteles.index, df_inventario_hoteles['id_hotel'], df_inventario_hoteles['fecha'])}
dict_idx_autos = {(a, f): i for i, a, f in zip(df_inventario_autos.index, df_inventario_autos['id_auto'], df_inventario_autos['fecha'])}
dict_idx_tours = {(t, f): i for i, t, f in zip(df_inventario_tours.index, df_inventario_tours['id_tour'], df_inventario_tours['fecha'])}

def generar_intencion_compra(id_venta, cliente):
    perfiles = ['Familiar', 'Negocios', 'Mochilero', 'Invitado Boda']
    perfil_viaje = random.choices(perfiles, weights=[0.35, 0.30, 0.20, 0.15], k=1)[0]
    
    destinos_validos = df_catalogo_vuelos['destino_iata'].unique().tolist()
    destinos_riviera = [d for d in ['CUN', 'CZM', 'TQO'] if d in destinos_validos]
    
    if perfil_viaje == 'Familiar':
        pasajeros, destino_iata, noches = random.randint(4, 9), random.choice(destinos_validos), random.randint(4, 7)
    elif perfil_viaje == 'Negocios':
        pasajeros, destino_iata, noches = random.randint(1, 2), random.choice([d for d in destinos_validos if d not in destinos_riviera]), random.randint(2, 3)
    elif perfil_viaje == 'Mochilero':
        pasajeros, destino_iata, noches = random.randint(1, 2), random.choice(destinos_validos), random.randint(5, 12)
    else: # Invitado Boda
        pasajeros, destino_iata, noches = random.randint(1, 3), random.choice(destinos_riviera), random.randint(3, 5)

    fecha_ida = datetime.strptime('2023-05-20', '%Y-%m-%d') + timedelta(days=random.randint(0, 1350))
    
    return {
        'id_venta': id_venta,
        'cliente': cliente,
        'perfil_viaje': perfil_viaje,
        'pasajeros': pasajeros,
        'destino_iata': destino_iata,
        'fecha_ida': fecha_ida.date(),
        'fecha_regreso': (fecha_ida + timedelta(days=noches)).date(),
        'noches_estancia': noches
    }

def reservar_vuelos_hash(intencion):
    destino, pasajeros = intencion['destino_iata'], intencion['pasajeros']
    fecha_ida, fecha_regreso = intencion['fecha_ida'], intencion['fecha_regreso']
    col_asientos = f"asientos_disponibles_{'premium' if intencion['perfil_viaje'] == 'Negocios' else 'eco'}"
    
    origen = 'CJS' if destino in aero_mx else 'ELP'
    rutas = df_catalogo_vuelos[(df_catalogo_vuelos['origen_iata'] == origen) & (df_catalogo_vuelos['destino_iata'] == destino)]['id_ruta'].tolist()
    
    if not rutas: return {"status": "Error"}
    id_ruta = rutas[0]
    
    for offset in [0, 1, 2, -1, -2]:
        f_ida, f_regreso = fecha_ida + timedelta(days=offset), fecha_regreso + timedelta(days=offset)
        idx_ida, idx_regreso = dict_idx_vuelos.get((id_ruta, f_ida)), dict_idx_vuelos.get((id_ruta, f_regreso))
        
        if (idx_ida is not None and df_itinerarios.at[idx_ida, col_asientos] >= pasajeros) and \
           (idx_regreso is not None and df_itinerarios.at[idx_regreso, col_asientos] >= pasajeros):
            
            df_itinerarios.at[idx_ida, col_asientos] -= pasajeros
            df_itinerarios.at[idx_regreso, col_asientos] -= pasajeros
            
            intencion.update({
                'fecha_ida_real': f_ida,
                'fecha_regreso_real': f_regreso,
                'noches_reales': (f_regreso - f_ida).days
            })
            return {"status": "Vendido", "ida": df_itinerarios.at[idx_ida, 'id_itinerario'], "regreso": df_itinerarios.at[idx_regreso, 'id_itinerario'], "intencion_act": intencion}
            
    return {"status": "Sold Out"}

def reservar_hotel_hash(intencion):
    destino, pasajeros, noches = intencion['destino_iata'], intencion['pasajeros'], intencion['noches_reales']
    fecha_llegada, perfil = intencion['fecha_ida_real'], intencion['perfil_viaje']
    
    cuartos = (pasajeros // 3) + (1 if pasajeros % 3 != 0 else 0)
    col_cuartos = 'cuartos_disponibles_vip' if perfil in ['Negocios', 'Invitado Boda'] else ('cuartos_disponibles_premium' if perfil == 'Familiar' else 'cuartos_disponibles_estandar')
        
    hoteles_dest = df_catalogo_hoteles[df_catalogo_hoteles['destino_iata'] == destino]['id_hotel'].tolist()
    
    for id_hotel in hoteles_dest:
        indices = [dict_idx_hoteles.get((id_hotel, fecha_llegada + timedelta(days=i))) for i in range(noches)]
        if all(idx is not None and df_inventario_hoteles.at[idx, col_cuartos] >= cuartos for idx in indices):
            for idx in indices: df_inventario_hoteles.at[idx, col_cuartos] -= cuartos
            return {"status": "Vendido", "id_hotel": id_hotel, "cuartos": cuartos}
            
    return {"status": "Sold Out"}

def reservar_extras_hash(intencion):
    perfil, destino, pasajeros = intencion['perfil_viaje'], intencion['destino_iata'], intencion['pasajeros']
    noches, fecha_llegada, id_hotel = intencion['noches_reales'], intencion['fecha_ida_real'], intencion.get('id_hotel')

    ticket = {'id_traslado': None, 'id_auto': None, 'id_seguro': None, 'id_tour': None}

    prob_auto = 0.8 if perfil == 'Negocios' else (0.4 if perfil == 'Familiar' else 0.05)
    
    if random.random() < prob_auto:
        cat = 'Van Familiar' if pasajeros >= 6 else ('SUV' if pasajeros >= 4 else 'Sedán')
        autos_disp = df_catalogo_autos[(df_catalogo_autos['aeropuerto_ubicacion'] == destino) & (df_catalogo_autos['categoria_auto'] == cat)]['id_auto'].tolist()
        
        if autos_disp:
            id_auto = random.choice(autos_disp)
            indices = [dict_idx_autos.get((id_auto, fecha_llegada + timedelta(days=i))) for i in range(noches)]
            if all(idx is not None and df_inventario_autos.at[idx, 'autos_disponibles'] >= 1 for idx in indices):
                for idx in indices: df_inventario_autos.at[idx, 'autos_disponibles'] -= 1
                ticket['id_auto'] = id_auto
                if random.random() < 0.8: ticket['id_seguro'] = df_catalogo_addons.sample(1).iloc[0]['id_addon']
    
    elif id_hotel:
        traslados = df_catalogo_traslados[df_catalogo_traslados['id_hotel_destino'] == id_hotel]
        if not traslados.empty: ticket['id_traslado'] = traslados.sample(1).iloc[0]['id_traslado']

    if perfil in ['Familiar', 'Invitado Boda'] and noches >= 2:
        tours = df_catalogo_tours[df_catalogo_tours['destino_iata'] == destino]['id_tour'].tolist()
        if tours:
            id_tour = random.choice(tours)
            idx = dict_idx_tours.get((id_tour, fecha_llegada + timedelta(days=1)))
            if idx is not None and df_inventario_tours.at[idx, 'lugares_disponibles'] >= pasajeros:
                df_inventario_tours.at[idx, 'lugares_disponibles'] -= pasajeros
                ticket['id_tour'] = id_tour

    return ticket

# ==========================================
# MÓDULO 4: EJECUCIÓN DE SIMULACIÓN Y EXPORTACIÓN
# ==========================================
print("Iniciando la simulación transaccional masiva...")

lista_compradores = []
for cliente in df_clientes['id_cliente'].tolist():
    lista_compradores.extend([cliente] * random.randint(1, 3))
random.shuffle(lista_compradores)

ventas_finales = []
for i, cliente in enumerate(lista_compradores):
    intencion = generar_intencion_compra(f"VTA-{100000 + i}", cliente)
    res_vuelo = reservar_vuelos_hash(intencion)
    
    if res_vuelo['status'] == 'Vendido':
        intencion_act = res_vuelo['intencion_act']
        res_hotel = reservar_hotel_hash(intencion_act)
        
        if res_hotel['status'] == 'Vendido':
            intencion_act['id_hotel'] = res_hotel['id_hotel']
            res_extras = reservar_extras_hash(intencion_act)
            
            ventas_finales.append({
                'id_venta': intencion_act['id_venta'], 'cliente': intencion_act['cliente'],
                'perfil_viaje': intencion_act['perfil_viaje'], 'pasajeros': intencion_act['pasajeros'],
                'destino_iata': intencion_act['destino_iata'], 'fecha_ida': intencion_act['fecha_ida_real'],
                'fecha_regreso': intencion_act['fecha_regreso_real'], 'noches': intencion_act['noches_reales'],
                'id_vuelo_ida': res_vuelo['ida'], 'id_vuelo_regreso': res_vuelo['regreso'],
                'id_hotel': res_hotel['id_hotel'], 'cuartos_reservados': res_hotel['cuartos'],
                **res_extras
            })

df_ventas_historicas = pd.DataFrame(ventas_finales)
print(f"Simulación exitosa. Total facturado: {len(df_ventas_historicas)} ventas consolidadas.")

print("Exportando modelos de datos a CSV...")
df_agentes.to_csv('dim_agentes.csv', index=False, encoding='utf-8')
df_clientes.to_csv('dim_clientes.csv', index=False, encoding='utf-8')
df_catalogo_vuelos.to_csv('dim_vuelos.csv', index=False, encoding='utf-8')
df_catalogo_hoteles.to_csv('dim_hoteles.csv', index=False, encoding='utf-8')
df_catalogo_tours.to_csv('dim_tours.csv', index=False, encoding='utf-8')
df_catalogo_autos.to_csv('dim_autos.csv', index=False, encoding='utf-8')
df_catalogo_traslados.to_csv('dim_traslados.csv', index=False, encoding='utf-8')
df_catalogo_addons.to_csv('dim_seguros.csv', index=False, encoding='utf-8')

df_itinerarios.drop(columns=['fecha_busqueda']).to_csv('inv_vuelos.csv', index=False, encoding='utf-8')
df_inventario_hoteles.to_csv('inv_hoteles.csv', index=False, encoding='utf-8')
df_inventario_tours.to_csv('inv_tours.csv', index=False, encoding='utf-8')
df_inventario_autos.to_csv('inv_autos.csv', index=False, encoding='utf-8')
df_ventas_historicas.to_csv('fact_ventas.csv', index=False, encoding='utf-8')

print("Proceso completo. 13 archivos exportados correctamente.")