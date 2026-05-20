import requests

url = "http://192.168.0.108:11434/api/chat"


messages = [
    {
        "role": "system",
        "content": "Eres un generador de titulares de noticias de un mundo simulado.",
    },{
    "role": "user",
    "content": """
        Tarea:
        Genera un titular de periódico para una simulación de ciudades.

        Contexto del mundo:
        - Existe una ciudad agrícola cuya principal exportación es comida.
        - Otras ciudades comenzaron a sufrir escasez de alimentos.
        - Las ciudades afectadas empezaron a comprar grandes cantidades de comida.

        Consecuencias:
        - Las ventas de la ciudad agrícola aumentaron.
        - La economía de la ciudad agrícola mejoró.
        - La crisis alimentaria comenzó a estabilizarse.

        Reglas:
        - El titular debe ser corto.
        - Máximo 15 palabras.
        - Debe sonar como una noticia económica o social.
        - Puede tener un tono ligeramente dramático o humorístico.
        - NO expliques el evento.
        - NO escribas párrafos.
        - SOLO responde con el titular.

        Formato obligatorio:
        Noticiero: [titular]
    """
}]

data = {
    "model": "llama3.1:8b",
    "messages": messages,
    "stream": False
}

response = requests.post(url, json=data)

print(response.json()["message"]["content"])