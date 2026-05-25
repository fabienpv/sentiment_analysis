from transformers import (
    AutoModelForSequenceClassification, AutoTokenizer
)
import torch
import json

from src.common import print_and_log_text, get_text_input
from src.config import PROJECT_DIR


# fr_emo_camembert_model = None
# fr_emo_camembert_tokenizer = None

fr_emo_detect_model = None
fr_emo_detect_tokenizer = None

# FR_EMO_CAMEMBERT_DIR = PROJECT_DIR / "french_emotion_camembert"

FR_EMO_DETECT_DIR = PROJECT_DIR / "emotions_detection_french"

## The model below does not contain disgust
# def get_fr_classifier():
#     global fr_emo_camembert_model
#     global fr_emo_camembert_tokenizer
#     if not fr_emo_camembert_model or not fr_emo_camembert_tokenizer:
#         fr_emo_camembert_model = AutoModelForSequenceClassification.from_pretrained(
#             str(FR_EMO_CAMEMBERT_DIR)
#         )
#         fr_emo_camembert_tokenizer = AutoTokenizer.from_pretrained(
#             str(FR_EMO_CAMEMBERT_DIR),
#             use_fast=False
#         )
#     return fr_emo_camembert_model, fr_emo_camembert_tokenizer


def get_fr_classifier_2():
    global fr_emo_detect_model
    global fr_emo_detect_tokenizer
    if not fr_emo_detect_model or not fr_emo_detect_tokenizer:
        fr_emo_detect_model = AutoModelForSequenceClassification.from_pretrained(
            str(FR_EMO_DETECT_DIR)
        )
        fr_emo_detect_tokenizer = AutoTokenizer.from_pretrained(
            str(FR_EMO_DETECT_DIR),
            use_fast=False
        )
    return fr_emo_detect_model, fr_emo_detect_tokenizer


key_mappings = {
    "dégout": "dégoût",
    "surpris": "surprise",
    "colere": "colère"
}

def run(text_input: str = None):
    json_path = PROJECT_DIR / "response" / "response_emotion_french.json"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path = str(json_path)

    with open(json_path, "w") as f_:
        f_.write("")

    if not text_input:
        text_input = get_text_input()
    if not text_input or len(text_input.strip()) == 0:
        exception_msg = "Error: text_input.txt seems empty."
        print_and_log_text(json_path, exception_msg)
        raise Exception(exception_msg)

    try:
        model, tokenizer = get_fr_classifier_2()
        inputs = tokenizer(text_input, return_tensors="pt", padding=True, truncation=True, max_length=512) 
        outputs = model(**inputs)


        with torch.no_grad(): # Use no_grad to save memory/compute during inference
            outputs = model(**inputs)

        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)[0]

        id2label = model.config.id2label

        json_response = {}
        for i, score in enumerate(probabilities):
            emotion_name = id2label[i]
            if emotion_name in key_mappings:
                emotion_name = key_mappings[emotion_name]
            json_response[emotion_name] = float(score.item())
        final_response = json.dumps(json_response, indent=4)

        print_and_log_text(json_path, final_response)

    except Exception as e:
        import traceback
        error_msg = f"Error when generating output: {str(e)}\n{traceback.format_exc()}"
        print_and_log_text(json_path, error_msg)
        json_response = {}

    return json_response


if __name__ == "__main__":
    run()

