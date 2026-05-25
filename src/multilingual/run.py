import torch
import json
from transformers import AutoProcessor, AutoModelForCausalLM
from typing import Literal

# Assuming these are your local imports
from src.common import print_and_log_text, get_text_input
from src.config import (
    PROJECT_DIR, get_system_prompt_en, get_system_prompt_fr, 
    MAX_NEW_TOKENS, DEFAULT_LANG, EMOTIONS
)


GEMMA_4_E2B = PROJECT_DIR / "gemma-4-E2B-it"


gemma_processor = None
gemma_model = None


def get_prompt_en(
    definitions: str,
    text_input: str
) -> str:
    return f"""## EMOTION DEFINITIONS:
{definitions}

## RULES:
Use the EMOTION DEFINITIONS to better understand what is meant by each emotion.

## TEXT TO ANALYZE:
{text_input}
"""

def get_prompt_fr(
    definitions: str,
    text_input: str
) -> str:
    return f"""## DEFINITIONS DES EMOTIONS:
{definitions}

## REGLES:
Utilise les définitions des émotions pour mieux comprendre ce que chaque émotion signifie.

## TEXT A ANALYSER
{text_input}
"""


def get_gemma_model():
    global gemma_model
    global gemma_processor
    if not gemma_model or not gemma_processor:
        # Load
        try:
            gemma_processor = AutoProcessor.from_pretrained(GEMMA_4_E2B)
            # Changed device_map to "cpu" and dtype to float32 for CPU compatibility
            gemma_model = AutoModelForCausalLM.from_pretrained(
                GEMMA_4_E2B,
                torch_dtype=torch.float32, 
                device_map="cpu"
            )
        except Exception as e:
            print(f"Error when loading Gemma 4 E2B: {e}")
    return gemma_model, gemma_processor
        

def run(
    lang: Literal["fr", "en"], 
    definitions: str = None,
    text_input: str = None
) -> tuple[dict[str, float], str]:
    """ Evaluates the emotions in the text using gemma 4 E2B model.
    Returns a tuple with:
    1) A dictionary with the emotion names for keys and the intensity for value (float bounded between 0 and 1)
    2) The reasoning (str)
    """
    file_path = PROJECT_DIR / "response" / "reasoning_Gemma_4_E2B.txt"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path = str(file_path)

    json_path = PROJECT_DIR / "response" / "response_Gemma_4_E2B.json"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path = str(json_path)

    # Clear the file at the start
    with open(file_path, "w") as f_:
        f_.write("")

    with open(json_path, "w") as f_:
        f_.write("")

    if lang == "fr":
        print_and_log_text(file_path, "Language: fr")
        system_prompt = get_system_prompt_fr()
    elif lang == "en":
        print_and_log_text(file_path, "Language: en")
        system_prompt = get_system_prompt_en()
    else:
        raise ValueError("Language must be 'fr' or 'en'")

    try:
        # 1. Load Processor
        model, processor = get_gemma_model()

        # 2. Prepare chat template
        if not text_input:
            text_input = get_text_input()
        if not text_input or len(text_input.strip()) == 0:
            exception_msg = "Error: text_input.txt seems empty."
            print_and_log_text(file_path, exception_msg)
            raise Exception(exception_msg)

        if not definitions:
            if lang == "fr":
                definitions = EMOTIONS["definitions_fr"]
            elif lang == "en":
                definitions = EMOTIONS["definitions_en"]

        prompt = text_input
        if definitions:
            if lang == "fr":
                prompt = get_prompt_fr(definitions, text_input)
            elif lang == "en":
                prompt = get_prompt_en(definitions, text_input)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        # 3. Process input using chat template
        prompt = processor.apply_chat_template(
            messages, 
            tokenize=False, 
            add_generation_prompt=True,
            enable_thinking=True
        )

        inputs = processor(text=prompt, return_tensors="pt").to("cpu")

        # 4. Generate output
        # Added max_new_tokens to ensure the process finishes and doesn't hang
        outputs = model.generate(
            **inputs, 
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=True,
            top_k=1,
            temperature=0.1
        )

        full_decoded = processor.decode(outputs[0], skip_special_tokens=True)

        print_and_log_text(file_path, f"FULL DECODED SEQUENCE: \n{full_decoded}")

        try:
            final_response = full_decoded.split("{")[1].split("}")[0].strip()
            final_response = "{" + final_response + "}"
            json_response = json.loads(final_response)
            for k, v in json_response.items():
                json_response[k] = int(v) / 100
            final_response = json.dumps(json_response, indent=4)
        except Exception as e:
            json_response = {}
            final_response = f"ERROR when decoding final response: {e}"

        print_and_log_text(json_path, final_response)

    except Exception as e:
        import traceback
        error_msg = f"Error when generating output: {str(e)}\n{traceback.format_exc()}"
        print_and_log_text(file_path, error_msg)
        json_response = {}
        full_decoded = error_msg

    return json_response, full_decoded


if __name__ == "__main__":
    run(DEFAULT_LANG)