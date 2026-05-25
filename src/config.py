from pathlib import Path
import copy

current_file = Path(__file__).resolve()

# Should not be changed
PROJECT_DIR = current_file.parent.parent

# Should be increased only if the output of Gemma-4 seems cropped. Useless for encoder models.
# Recommended values are powers of 2 (e.g. 2048, 4096, 8192)
MAX_NEW_TOKENS = 4096

# Write "7" for the model emotion-english-distilroberta-base
# Write "28" for the model emotion-english-distilroberta-base
DEFAULT_ENGLISH_EMOTIONS = "7" # allowed options: "7", "28"

# Default language option for Gemma 4. "en" is recommended to analyze english text
# whereas "fr" is recommended to analyze french text.
DEFAULT_LANG = "fr" # allowed options: "en" or "fr"

# the structure of the dictionary should not change: same keys, same type (lists of text strings) as values
# However, the content of text strings can be modified: emotions can be replaced, added, removed.
# definitions in french or in english can be provided as text string in the dictionary.
# The definitions, if any, are given to Gemma 4 as context to evaluate more precisely the emotions
# in the text.
EMOTIONS = {
"en": [
    "anger",
    "disgust",
    "fear",
    "joy",
    "sadness",
    "surprise",
],

"fr": [
    "colère",
    "dégoût",
    "peur",
    "joie",
    "tristesse",
    "surprise",
],

"definitions_fr": [],

"definitions_en": []
}


def list_to_str(_list_):
    list_copy = copy.copy(_list_)
    list_copy = [f"- {l_}" for l_ in list_copy]
    return "\n".join(list_copy)


# The functions below are the system prompts, in fr and en, containing the main 
# instruction for the analyzes of emotions in the text.
def get_system_prompt_en():
    return f""" You are an expert english psychological linguist specializing in sentiment analysis and emotion analysis. \
Your task is to analyze the provided text and quantify the intensity of specific emotions present within it.

## EMOTIONS TO EVALUATE
{list_to_str(EMOTIONS["en"])}

## SCORE RULES
- For each emotion, assign a score between 0 and 100.
- 0 indicates the complete absence of that emotion.
- 100 indicates the extreme, overwhelming presence of that emotion.
- Multiple emotions can coexist and the scores should reflect all present emotion intensities.

## OUTPUT
You must respond only with a valid JSON dictionary.
Do not include any introductory text, explanations, markdown formatting (like ```json), \
or concluding remarks. The keys must be the exact emotion names listed above and the values should be the score.
"""

def get_system_prompt_fr():
    return f"""Tu es un expert en linguistique psychologique, spécialisé dans l'analyse des sentiments et l'analyse des émotions. \
Ta tâche consiste à analyser le texte fourni et à quantifier l'intensité des émotions qui s'y trouvent.

## ÉMOTIONS À ÉVALUER
{list_to_str(EMOTIONS["fr"])}

## RÈGLES DE NOTATION
- Pour chaque émotion, attribue un score compris entre 0 et 100.
- 0 indique l'absence totale de cette émotion.
- 100 indique la présence extrême et envahissante de cette émotion.
- Plusieurs émotions peuvent coexister et les scores doivent refléter l'intensité de toutes les émotions présentes.

## FORMAT DE SORTIE
Réponds uniquement avec un dictionnaire JSON valide.
N'inclue aucun texte d'introduction, aucune explication, aucun formatage markdown (pas de ```json), \
ni aucune remarque de conclusion. Les clés doivent être les noms exacts des émotions listées ci-dessus et les valeurs doivent être les scores.
"""