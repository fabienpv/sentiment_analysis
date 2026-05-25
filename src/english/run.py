from transformers import pipeline

from src.common import pipeline_text_classification
from src.config import PROJECT_DIR

from typing import Literal


en_distilroberta_model = None
en_roberta_go_emotions = None

EMO_EN_DISTILROBERTA_DIR = PROJECT_DIR / "emotion-english-distilroberta-base"
ROBERTA_GO_EMO_DIR = PROJECT_DIR / "roberta-base-go_emotions"

def get_en_classifier_7():
    global en_distilroberta_model
    if not en_distilroberta_model:
        en_distilroberta_model = pipeline(
            "text-classification", 
            model=str(EMO_EN_DISTILROBERTA_DIR), 
            return_all_scores=True
        )
    return en_distilroberta_model

def get_en_classifier_28():
    global en_roberta_go_emotions
    if not en_roberta_go_emotions:
        en_roberta_go_emotions = pipeline(
            "text-classification", 
            model=str(ROBERTA_GO_EMO_DIR), 
            return_all_scores=True
        )
    return en_roberta_go_emotions

def run(
    text_input: str = None,
    mode: Literal["7", "28", "both"] = "both"
) -> dict[str, float] | tuple[dict[str, float], dict[str, float] ]:
    """Classifies the text in 7 or 28 emotion categories in the text using emotion-english-distilroberta-base
    or "roberta-base-go_emotions".
    Returns either a dictionary with the emotion names for keys and the intensity for value 
    (float bounded between 0 and 1) if a single mode == "7" or mode == "28", else return a tuple
    with 2 of such dictionaries, one for each model.
    """
    json_response = None

    if str(mode) != "28":
        json_path = PROJECT_DIR / "response" / "response_emotion_english_distilroberta.json"
        classifier = get_en_classifier_7()
        json_response = pipeline_text_classification(classifier, json_path, text_input)

    if str(mode) != "7":
        json_path = PROJECT_DIR / "response" / "response_roberta_go_emotions.json"
        classifier = get_en_classifier_28()
        output = pipeline_text_classification(classifier, json_path, text_input)
        if json_response:
            json_response = (json_response, output)
        else:
            json_response = output
    
    return json_response


if __name__ == "__main__":
    run()

