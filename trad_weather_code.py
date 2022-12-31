def decode_weather(weather):
    """Traduit le weathercode en français pour la lisibilité"""
    weathercodes = weather['weathercode']
    climate = []
    for weathercode in weathercodes:
        if weathercode == 0:
            climate.append('Clair')
        elif 1 <= weathercode <= 3:
            climate.append('Nuageux')
        elif weathercode == 45 or weathercode == 48:
            climate.append('Brouillard')
        elif 51 <= weathercode <= 67:
            climate.append('Pluie')
        elif 71 <= weathercode <= 77:
            climate.append('Neige')
        elif 80 <= weathercode <= 82:
            climate.append('Pluie')
        elif weathercode == 85 and weathercode == 86:
            climate.append('Neige')
        elif weathercode > 90:
            climate.append('Tempete')
    return climate
