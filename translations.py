from googletrans import Translator
import asyncio
import concurrent.futures

TRANSLATIONS = {
    'en': {
        'search_city': 'Search your city',
        'city_not_found': 'No city with name {city_name} was found.\nTry to enter the full city name and the country',
        'understood': 'Understood',
        'search_example': 'Example: Saint Petersburg, USA',
        'spf_not_req': 'Not Required',
        'uv': 'UV index: ',
        'high_uv': 'High',
        'moderate_uv': 'Moderate',
        'low_uv': 'Low',
        'vitamin_d': 'Vitamin D',
        'no_vitamin_d': 'Vitamin D synthesis unlikely',
        'time_till_burn': 'Time till burn',
        'air_low': 'Low',
        'air_moderate': 'Moderate',
        'air_high': 'High',
        'aqi_good': 'Good',
        'aqi_moderate': 'Moderate',
        'aqi_critical': 'Critical',
        'set_button': 'Set',
        'your_city': 'Your city: ',
        'wind': 'Wind Speed',
        'sun': 'Sun Time',
        'aqi': 'Air Quality: ',
        'water': 'Sea Temperature',
        'time': 'Time',
        'today': 'Today',
        'monday': 'Monday',
        'tuesday': 'Tuesday',
        'wednesday': 'Wednesday',
        'thursday': 'Thursday',
        'friday': 'Friday',
        'saturday': 'Saturday',
        'sunday': 'Sunday',
        'sunrise': 'Sunrise time: ',
        'sunset': 'Sunset time: ',
        'open_map': 'Find sunscreen nearby',
        'advices': 'Advices',
        'hide_advices': 'Hide Advices',
        'imperial_units': 'Imperial',
        'metric_units': 'Metric',
        'units': 'Units',
        'welcome': 'Welcome to UVify!',
        'start_following': 'Start following your city',
        'from_torre': 'Are you from Torredembarra?',
        'settings': 'Settings',
        'skin': 'Your skin color',
        'track_nav': 'Track',
        'weather_nav': 'Weather',
        'loading': 'Loading...',
        'change_lang': 'Change the language',
        'restart_app': 'To change the language, restart the application, please',
        'current_time': 'Current time: ',
        'language': 'Language',
        'pale': 'Pale',
        'fair': 'Fair',
        'medium': 'Medium',
        'olive': 'Olive',
        'brown': 'Brown',
        'dark_brown': 'Dark Brown',
        # 'perm_title': 'Geolocation request',
        # 'perm_descr': 'If you want to see your location on the map (optional), please allow the app to access your location.',
        # 'perm_action1': 'Request access',
        # 'perm_action2': 'Never remind',


    },

    'es': {
        'search_city': 'Busca tu ciudad',
        'city_not_found': 'No se encontró ninguna ciudad con el nombre {city_name}.\nIntenta introducir el nombre completo de la ciudad y el país.',
        'understood': 'Entendido',
        'search_example': 'Ejemplo: Madrid, España',
        'spf_not_req': 'No se require',
        'uv': 'Índice UV: ',
        'high_uv': 'Alto',
        'moderate_uv': 'Moderado',
        'low_uv': 'Bajo',
        'vitamin_d': 'Vitamina D',
        'time_till_burn': 'Tiempo hasta quemarse',
        'no_vitamin_d': 'Síntesis de vitamina D poco probable',
        'air_low': 'Baja',
        'air_moderate': 'Moderada',
        'air_high': 'Alta',
        'aqi_good': 'Buena',
        'aqi_moderate': 'Moderada',
        'aqi_critical': 'Crítica',
        'set_button': 'Establecer',
        'your_city': 'Tu ciudad: ',
        'wind': 'Velocidad del viento',
        'sun': 'Tiempo del Sol',
        'aqi': 'Calidad del Aire: ',
        'water': 'Temperatura del mar',
        'time': 'Tiempo',
        'today': 'Hoy',
        'monday': 'Lunes',
        'tuesday': 'Martes',
        'wednesday': 'Miércoles',
        'thursday': 'Jueves',
        'friday': 'Viernes',
        'saturday': 'Sábado',
        'sunday': 'Domingo',
        'sunrise': 'Amanecer: ',
        'sunset': 'Atardecer: ',
        'open_map': 'Encontrar protector solar cerca',
        'advices': 'Consejos',
        'hide_advices': 'Esconder consejos',
        'imperial_units': 'Imperiales',
        'metric_units': 'Métricas',
        'units': 'Unidades',
        'welcome': 'Bienvenido/a a UVify!',
        'start_following': 'Empezar a seguir tu ciudad',
        'from_torre': 'Eres de Torredembarra?',
        'settings': 'Ajustes',
        'skin': 'Color de piel',
        'track_nav': 'Seguir',
        'weather_nav': 'Tiempo',
        'loading': 'Cargando...',
        'change_lang': 'Cambio del idioma',
        'restart_app': 'Para cambiar el idioma, reinicia the applicación, por favor',
        'current_time': 'Hora actual: ',
        'language': 'Idioma',
        'pale': 'Pálida',
        'fair': 'Clara',
        'medium': 'Media',
        'olive': 'Oliva',
        'brown': 'Castaño',
        'dark_brown': 'Castaño oscuro',
        # 'perm_title': 'Solicitud de geolocalización',
        # 'perm_descr': 'Si desea ver su ubicación en el mapa (opcional), permita que la aplicación acceda a ella',
        # 'perm_action1': 'Solicitar acceso',
        # 'perm_action2': 'No recordar',
    }
}



def t(key, lang='en', **kwargs):

    output_text = TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

    return output_text.format(**kwargs)





async def translate_city(text, src='es', dest='en'):
    async with Translator() as translator:
        result = await translator.translate(text, src=src, dest=dest)

    return result

def run_async(coro):
    with concurrent.futures.ThreadPoolExecutor() as pool:
        return pool.submit(lambda: asyncio.run(coro)).result()










