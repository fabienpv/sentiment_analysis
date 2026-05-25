import json
import re

from src.config import PROJECT_DIR

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from transformers import Pipeline
    from pathlib import Path


def print_and_log_text(path: str, text: str):
    with open(path, "a") as f_:
        f_.write(text)
    print(text)


def get_text_input():
    with open(str(PROJECT_DIR / "text_input.txt"), "r", encoding="utf-8") as f_:
        text = f_.read()
    return text.strip()


def pipeline_text_classification(
    classifier: 'Pipeline',
    json_path: 'Path',
    text_input: str = None,
) -> dict[str, float] | tuple[dict[str, float], dict[str, float] ]:
    """Classifies the text in X emotion categories in the text using transformers text-classification pipeline.
    Returns a dictionary with the emotion names for keys and the intensity for value (float bounded between 0 and 1)
    """
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path = str(json_path)

    # Clear the file at the start
    with open(json_path, "w") as f_:
        f_.write("")

    if not text_input:
        text_input = get_text_input()
    if not text_input or len(text_input.strip()) == 0:
        exception_msg = "Error: text_input.txt seems empty."
        print_and_log_text(json_path, exception_msg)
        raise Exception(exception_msg)

    try:
        output = classifier(text_input, top_k=None)

        print(output)
        json_response = {}
        for item in output:
            json_response[item["label"]] = item["score"]

        final_response = json.dumps(json_response, indent=4)
        print_and_log_text(json_path, final_response)

    except Exception as e:
        import traceback
        error_msg = f"Error when generating output: {str(e)}\n{traceback.format_exc()}"
        print_and_log_text(json_path, error_msg)
        json_response = {}
        
    return json_response


def sentence_splitter(text_input: str):
    splits = re.split(r"[\.;:]", text_input)
    sentences = []
    ongoing = ""
    for s in splits:
        if len(f"{ongoing};{s}") > 60:
            if ongoing:
                sentences.append(f"{ongoing};{s}".strip())
            else:
                sentences.append(f"{ongoing}{s}".strip())
            ongoing = ""
        else:
            ongoing += f";{s}"
    if ongoing:
        sentences.append(f"{ongoing};{s}".strip())
    sentences = [s for s in sentences if s.strip()]
    return sentences



def calculate_average(data):
    if not data:
        return {}

    emotion_sums = {}
    count = len(data)

    for entry in data:
        emotions = entry.get("emotions", {})
        for emotion, value in emotions.items():
            emotion_sums[emotion] = emotion_sums.get(emotion, 0) + value

    return {emotion: total / count for emotion, total in emotion_sums.items()}

def calculate_min(data):
    if not data:
        return {}

    # Initialize mins with the first entry's emotions
    mins = data[0]["emotions"].copy()

    for entry in data[1:]:
        emotions = entry.get("emotions", {})
        for emotion, value in emotions.items():
            if emotion in mins:
                mins[emotion] = min(mins[emotion], value)
            else:
                # If the emotion wasn't in the first entry, initialize it
                mins[emotion] = value
    return mins

def calculate_max(data):
    if not data:
        return {}

    # Initialize maxs with the first entry's emotions
    maxs = data[0]["emotions"].copy()

    for entry in data[1:]:
        emotions = entry.get("emotions", {})
        for emotion, value in emotions.items():
            if emotion in maxs:
                maxs[emotion] = max(maxs[emotion], value)
            else:
                # If the emotion wasn't in the first entry, initialize it
                maxs[emotion] = value
    return maxs


def stats_summary(json_path: 'Path', stats_path: 'Path') -> list[dict] | None:

    json_path.parent.mkdir(parents=True, exist_ok=True)
    if json_path.exists():
        try:
            json_path = str(json_path)
            stats_path = str(stats_path)
            with open(json_path, "r") as f_:
                results = json.loads(f_.read())

            n_sentences = len(results)
            avg = calculate_average(results)
            mins = calculate_min(results)
            maxs = calculate_max(results)

            final_json = {
                "n": n_sentences,
                "average": avg,
                "minima": mins,
                "maxima": maxs
            }

            final_answer = json.dumps(final_json, indent=4)

            print_and_log_text(stats_path, final_answer)
            
        except Exception as e:
            import traceback
            error_msg = f"Error when generating sentences stats summary: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            final_json = {}

        return final_json
            
