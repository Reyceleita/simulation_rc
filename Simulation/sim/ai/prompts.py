"""
prompts.py

Prompts utilizados por el sistema de noticias.
"""

from random import choice


# -------------------------------------------------------------
# Prompt del sistema
# -------------------------------------------------------------

SYSTEM_PROMPT = """
Eres el periodista principal de "Sin presupuesto para humanos".

Personalidad:

- Algo Profesional.
- Algo serio.
- Ligeramente sarcástico.
- El humor debe ser ligeramente evidente.
- Nunca hagas bromas absurdas.
- Escribes para un periódico económico y otras cosas.

Contexto:

Las noticias pertenecen a un mundo simulado compuesto por 4 ciudades.

Reglas:

- Máximo 15 palabras.
- Solo un titular.
- No expliques nada.
- No escribas párrafos.
- No uses comillas.
- No inventes personajes famosos.
- No rompas la cuarta pared.
- Debe parecer un periódico real.
- No usas nombres de ciudades

Formato obligatorio:

Noticiero: [titular]
"""


# -------------------------------------------------------------
# Construcción del prompt
# -------------------------------------------------------------

def build_prompt(topic: str, history: list[str]) -> str:
    """
    Construye el prompt que recibirá Ollama.
    """

    history_text = ""

    if history:

        history_text = "\n".join(
            f"- {news}"
            for news in history[-10:]
        )

    situations = {

        "Economía": [
            "La economía de varias ciudades muestra señales inesperadas.",
            "Los comerciantes hablan de una jornada inusual.",
            "El mercado atraviesa cambios importantes."
        ],

        "Agricultura": [
            "Las cosechas fueron mejores de lo esperado.",
            "Los agricultores comentan una temporada diferente.",
            "La producción agrícola sorprendió al mercado."
        ],

        "Industria": [
            "Las fábricas trabajan a buen ritmo.",
            "La producción industrial aumentó.",
            "Los talleres viven una semana especialmente activa."
        ],

        "Transporte": [
            "El comercio entre ciudades aumenta.",
            "Las rutas comerciales estuvieron muy ocupadas.",
            "Los transportistas no descansan."
        ],

        "Ciudadanos": [
            "Los habitantes reaccionan a los cambios económicos.",
            "Los ciudadanos comentan los últimos acontecimientos.",
            "Las plazas están llenas de rumores."
        ]
    }

    context = choice(
        situations.get(
            topic,
            ["Ha ocurrido un hecho curioso en una ciudad."]
        )
    )

    return f"""
Tema:

{topic}

Situación:

{context}

Noticias recientes:

{history_text if history_text else "Ninguna"}

Genera un titular completamente diferente a los anteriores.

Recuerda:

- Máximo 15 palabras.
- Solo el titular.
- Formato:
Noticiero: ...
"""