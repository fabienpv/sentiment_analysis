import json

from src.common import (
    sentence_splitter, print_and_log_text, get_text_input,
    stats_summary
)
from src.english.run import run as run_en
from src.config import PROJECT_DIR, DEFAULT_ENGLISH_EMOTIONS

from typing import Literal


def run(
    text_input: str = None, 
    mode: Literal["7", "28"] = DEFAULT_ENGLISH_EMOTIONS
) -> list[dict]:

    assert str(mode) in ["7", "28"], str(mode)

    json_path = PROJECT_DIR / "response" / "response_per_sentence__emotion_english.json"
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
    
    sentences = sentence_splitter(text_input)

    results = []
    for sentence in sentences:
        response = {"sentence": sentence}
        response["emotions"] = run_en(sentence, mode)
        results.append(response)

    final_response = json.dumps(results, indent=4)

    print_and_log_text(json_path, final_response)
    
    return results


def stats() -> dict[str, dict]:

    json_path = PROJECT_DIR / "response" / "response_per_sentence__emotion_english.json"
    stats_path = PROJECT_DIR / "response" / "stats_response_per_sentence__emotion_english.json"
    
    return stats_summary(json_path, stats_path)
            


if __name__ == "__main__":
    run()
    stats()