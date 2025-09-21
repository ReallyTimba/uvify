from googletrans import Translator

TRANSLATIONS = {
    'en': {
        'search_city': 'Search your city',
        'city_not_found': 'No city with name {city_name} was found.\nTry to enter the full city name and the country',
        'understood': 'Understood',
        'search_example': 'Example: Saint Petersburg, USA',
        'spf_not_req': 'Not Required',
        'uv': 'UV index: ',
        'high_uv': 'High',
        'moderate_uv': 'Moderate UV',
        'low_uv': 'Low UV',
        'vitamin_d': 'Vitamin D',
        'time_till_burn': 'Time till burn',
        'air_good': 'Good',
        'air_moderate': 'Moderate',
        'air_critical': 'Very High',
        'set_button': 'Set',
        'your_city': 'Your city: ',
        'wind': 'Wind Speed',
        'sun': 'Sun Time',
        'aqi': 'Air Quality',
        'water': 'Sea Temperature',
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
        'dark_brown': 'Dark Brown'

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
        'air_good': 'Buena',
        'air_moderate': 'Moderada',
        'air_critical': 'Muy alta',
        'set_button': 'Establecer',
        'your_city': 'Tu ciudad: ',
        'wind': 'Velocidad del viento',
        'sun': 'Tiempo del Sol',
        'aqi': 'Calidad del Aire',
        'water': 'Temperatura del mar',
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
        'dark_brown': 'Castaño oscuro'
    }
}



def t(key, lang='en', **kwargs):

    output_text = TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

    return output_text.format(**kwargs)





async def translate_city(text, src='es', dest='en'):
        async with Translator() as translator:
            result = await translator.translate(text, src=src, dest=dest)

        return result












