"""
Módulo de análisis jurídico de folios de matrícula inmobiliaria colombiana.
Implementa:
1. Motor de reglas determinísticas (detección de falsas tradiciones, embargos, hipotecas, tracto sucesivo).
2. Conexión con LLM a través de OpenRouter (con salvaguarda anti-alucinaciones y corpus).
"""

import os
import re
import json
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def load_system_prompt() -> str:
    prompt_path = BASE_DIR / "prompts" / "system_prompt_v1.md"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    return "Eres un asistente jurídico experto en derecho inmobiliario y registral colombiano."

def load_corpus_summary() -> str:
    corpus_dir = BASE_DIR / "corpus"
    summary_parts = []
    if corpus_dir.exists():
        for file in sorted(corpus_dir.glob("*.md")):
            summary_parts.append(f"--- FUENTE: {file.name} ---\n" + file.read_text(encoding="utf-8")[:1500])
    return "\n\n".join(summary_parts)

def analyze_locally(text: str) -> dict:
    """
    Analizador determinístico basado en el marco de la Ley 1579 de 2012 y Código Civil.
    Procesa el texto de las anotaciones y extrae hallazgos jurídicos clave.
    """
    text_lower = text.lower()
    findings = []
    alerts = []
    semaphore = "VERDE"
    reasons = []

    # 1. Detección de Falsa Tradición (Columna 6 / Art. 7 Ley 1579)
    falsa_patterns = [
        r"columna 6",
        r"falsa tradici[oó]n",
        r"posesi[oó]n inscrita",
        r"derechos y acciones herenciales",
        r"venta de derechos herenciales",
        r"mejora en suelo ajeno"
    ]
    has_falsa_tradicion = any(re.search(p, text_lower) for p in falsa_patterns)
    if has_falsa_tradicion:
        semaphore = "ROJO"
        msg = "Se detectó indicio de FALSA TRADICIÓN (Columna 6 / Art. 7 Ley 1579 de 2012). El tradente no cuenta con dominio pleno y se requiere saneamiento judicial."
        alerts.append(msg)
        reasons.append("Falsa Tradición detectada")

    # 2. Detección de Medidas Cautelares / Embargos (Columna 3)
    has_embargo = "embargo" in text_lower or "demanda sobre" in text_lower or "medida cautelar" in text_lower
    has_desembargo = "desembargo" in text_lower or "cancelaci[oó]n de embargo" in text_lower or "cancelacion de medida" in text_lower
    if has_embargo and not has_desembargo:
        semaphore = "ROJO"
        msg = "Se detectó MEDIDA CAUTELAR / EMBARGO VIGENTE sin constancia de cancelación. Conforme al Art. 1521 Núm. 3 del Código Civil, el bien se encuentra fuera del comercio."
        alerts.append(msg)
        reasons.append("Embargo judicial vigente")

    # 3. Detección de Ruptura de Tracto Sucesivo
    if "ruptura" in text_lower or "eslab[oó]n faltante" in text_lower:
        semaphore = "ROJO"
        msg = "Se detectó posible RUPTURA DE TRACTO SUCESIVO (Art. 3 Numeral 4 Ley 1579 de 2012). El enajenante no coincide con el adquirente del registro anterior."
        alerts.append(msg)
        reasons.append("Ruptura del principio de tracto sucesivo")

    # 4. Detección de Gravámenes Hipotecarios (Columna 2)
    has_hipoteca = "hipoteca" in text_lower
    has_cancel_hipoteca = "cancelaci[oó]n de hipoteca" in text_lower or "cancelacion hipoteca" in text_lower
    if has_hipoteca and not has_cancel_hipoteca:
        if semaphore != "ROJO":
            semaphore = "AMARILLO"
        msg = "Se identificó HIPOTECA ACTIVA (Columna 2). Se requiere minuta de cancelación de hipoteca expedida por la entidad acreedora previa o simultánea a la escrituración."
        alerts.append(msg)
        reasons.append("Hipoteca vigente pendiente de cancelación")

    # 5. Detección de Limitaciones al Dominio (Columna 4)
    has_vivienda_fam = "afectaci[oó]n a vivienda familiar" in text_lower or "afectacion a vivienda" in text_lower or "ley 258" in text_lower
    has_patrimonio_fam = "patrimonio de familia" in text_lower
    if has_vivienda_fam or has_patrimonio_fam:
        if semaphore != "ROJO":
            semaphore = "AMARILLO"
        msg = "Se identificó LIMITACIÓN AL DOMINIO (Afectación a Vivienda Familiar o Patrimonio de Familia). Requiere firma de ambos cónyuges/compañeros para su levantamiento (Ley 258/1996)."
        alerts.append(msg)
        reasons.append("Limitación al dominio (Vivienda Familiar / Patrimonio de Familia)")

    # 6. Evaluación General
    if semaphore == "VERDE":
        reasons.append("Tracto sucesivo continuo y folio aparentemente libre de gravámenes o medidas cautelares activas.")

    return {
        "semaphore": semaphore,
        "reasons": reasons,
        "alerts": alerts,
        "normas_aplicadas": [
            "Ley 1579 de 2012 (Estatuto de Registro de Instrumentos Públicos)",
            "Código Civil Colombiano (Arts. 740, 756, 1521, 2432)",
            "Decreto 960 de 1970 (Estatuto Notarial)",
            "Ley 258 de 1996 (Afectación a Vivienda Familiar)"
        ]
    }

def analyze_with_openrouter(text: str, api_key: str, model: str = "meta-llama/llama-3.3-70b-instruct:free") -> str:
    """
    Envía las anotaciones al LLM a través de la API de OpenRouter, incorporando
    el prompt del sistema y las normas del corpus.
    """
    system_prompt = load_system_prompt()
    corpus_context = load_corpus_summary()

    full_system = f"""{system_prompt}

### CORPUS NORMATIVO APLICABLE (CITA SIEMPRE ESTAS NORMAS):
{corpus_context}
"""

    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/JacoboPC/Clase-derecho-IA-2026-II",
        "X-Title": "Automatizacion Estudios de Titulos - Javeriana"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": full_system},
            {"role": "user", "content": f"Por favor realiza el estudio de títulos completo del siguiente caso registral:\n\n{text}"}
        ],
        "temperature": 0.1
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        data=json.dumps(payload),
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(f"Error de OpenRouter ({response.status_code}): {response.text}")

    data = response.json()
    return data["choices"][0]["message"]["content"]
