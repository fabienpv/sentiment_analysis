# INSTALLATION

1. Install Python (preferably Python 3.12) ([https://www.python.org/downloads/release/python-3120/](https://www.python.org/downloads/release/python-3120/))

2. Install Git ([https://git-scm.com/install/](https://git-scm.com/install/))

3. Open PowerShell or CMD.

4. In PowerShell or CMD, navigate to the folder where you want to add the project repository:
```bash
cd C:\Users\myusername\Documents\pick_a_repo
```

5. Clone the project repository:
```bash
git clone https://github.com/fabienpv/sentiment_analysis.git
```

6. Move into the project repository:
```bash
cd sentiment_analysis
```

7. Create a virtual environment (recommended name: `.venv`)
```bash
python -m venv .venv
```

8. Activate the virtual environment to download the required libraries inside.
```bash
source .venv/Scripts/activate
```

9. Install the required libraries. This may take a few minutes:
```bash
pip install -r requirements.txt
```

10. Clone the model repositories from Hugging Face. This may take several minutes per model:
```bash
git clone https://huggingface.co/google/gemma-4-E2B-it
```
```bash
git clone https://huggingface.co/j-hartmann/emotion-english-distilroberta-base
```
```bash
git clone https://huggingface.co/ac0hik/emotions_detection_french
```
```bash
git clone https://huggingface.co/SamLowe/roberta-base-go_emotions
```

After installation, the project directory structure should look like this:

```text
sentiment_analysis
|___.venv/
|___emotion-english-distilroberta-base/
|___emotion_detection_french/
|___gemma-4-E2B-it/
|___roberta-base-go_emotions/
|___src/
|___tests/
|___LICENSE
|___README.md
|___requirements.txt
|___text_input.txt
```

# HOW TO USE

The executable Python scripts are:

`src.english.run.py`
`src.english.run_per_sentence.py`
`src.french.run.py`
`src.french.run_per_sentence.py`
`src.multilingual.run.py`
`src.gui.py`

1. Open PowerShell or CMD.

2. Navigate to the project directory:
```bash
cd C:\Users\myusername\Documents\pick_a_repo\sentiment_analysis
```

3. Activate the virtual environment. It will let python know where to find the libraries needed for the script.
```bash
source .venv/Scripts/activate
```

4. To run the GUI:
```bash
python -m streamlit run src/gui.py
```

To run the `run*.py` scripts:

First, write the text you wish to process in `text_input.txt`. 
Then, run the script using `python -m`. 

Example:
```bash
python -m src.french.run
```

The results will be displayed in your terminal (CMD or PowerShell window).

# RUNNERS

**src.english.run.py**
Runs encoder models (`roberta-base-go_emotions` and `emotion-english-distilroberta-base`) trained on English text.
The models will process the entire text in `text_input.txt` in a single run (one analysis for the full text).

`emotion-english-distilroberta-base` will return results for 6 emotions + a neutral state.
The output will be saved in `response\response_emotion_english_distilroberta.json`.

Example: 
```json
{
    "neutral": 0.7033904194831848,
    "sadness": 0.12923076748847961,
    "joy": 0.04061059281229973,
    "surprise": 0.03869979828596115,
    "disgust": 0.036024462431669235,
    "fear": 0.029594385996460915,
    "anger": 0.022449685260653496
}
```

`roberta-base-go_emotions` will return results for 27 emotions + a neutral state.
The output will be saved in `response\response_roberta_go_emotions.json`.

Example: 
```json
{
    "neutral": 0.6146126985549927,
    "annoyance": 0.13241127133369446,
    "disapproval": 0.0903424322605133,
    "approval": 0.08127696812152863,
    "disgust": 0.04841749742627144,
    "realization": 0.029497023671865463,
    "disappointment": 0.02932540699839592,
    "anger": 0.0071326373144984245,
    "sadness": 0.005613381043076515,
    "embarrassment": 0.005178698338568211,
    "fear": 0.004492246545851231,
    "optimism": 0.0030622142367064953,
    "confusion": 0.002597152953967452,
    "admiration": 0.0020021626260131598,
    "caring": 0.0016922670183703303,
    "desire": 0.001564397127367556,
    "curiosity": 0.0013620347017422318,
    "nervousness": 0.0009554177522659302,
    "amusement": 0.0006578426691703498,
    "relief": 0.00062993896426633,
    "love": 0.0005961807910352945,
    "surprise": 0.0005632443353533745,
    "grief": 0.0004863603680860251,
    "remorse": 0.0004657526151277125,
    "excitement": 0.0004295211401768029,
    "pride": 0.0003633831802289933,
    "joy": 0.0003591400745790452,
    "gratitude": 0.000341276841936633
}
```

**Notes:** 
- The models provide emotion probabilities; the sum of all scores should equal 1 (or approximately 1 with `roberta-base-go_emotions`). 
- The models were likely trained on relatively short texts.
- Because the models were likely trained on single-class text, they may overestimate the probability of the primary emotion and underestimate the probability of all other emotions.
- The scores represent emotion probabilities, not emotion intensities.

**src.english.run_per_sentence.py**

Since the models may have been trained on short texts, this runner splits the text into individual sentences and performs sentiment analysis on each sentence separately.

The result for each sentence is saved in `response\response_per_sentence_emotion_english.json`.
A statistical summary (containing the number of sentences, average scores per emotion, and the maximum/minimum scores per emotion across all sentences) is saved in `response\stats_response_per_sentence_emotion_english.json`.

Example of result per sentence:
```json
[
    {
        "sentence": "For most consumers, packaged meat appears clean, fresh, and safe",
        "emotions": {
            "neutral": 0.775077760219574,
            "disgust": 0.10167603194713593,
            "joy": 0.09944059699773788,
            "anger": 0.00858047790825367,
            "surprise": 0.007027977611869574,
            "sadness": 0.006482393480837345,
            "fear": 0.0017147940816357732
        }
    },
    {
        "sentence": "The reality of industrial meat production is biologically repulsive",
        "emotions": {
            "disgust": 0.9473800659179688,
            "fear": 0.030567234382033348,
            "anger": 0.007733263541013002,
            "sadness": 0.005891242064535618,
            "neutral": 0.0057511418126523495,
            "surprise": 0.0020291469991207123,
            "joy": 0.0006479627336375415
        }
    }
]
```

Example of statistical summary:
```json
{
    "n": 21,
    "average": {
        "neutral": 0.13927524128840083,
        "disgust": 0.7930790737626099,
        "joy": 0.00778089597588405,
        "anger": 0.02900789731315204,
        "surprise": 0.006047995068088528,
        "sadness": 0.013498140997918589,
        "fear": 0.011310742674617185
    },
    "minima": {
        "neutral": 0.0035214992240071297,
        "disgust": 0.036024462431669235,
        "joy": 0.0001987586438190192,
        "anger": 0.0028946087695658207,
        "surprise": 0.0005867864820174873,
        "sadness": 0.0017678223084658384,
        "fear": 0.0017147940816357732
    },
    "maxima": {
        "neutral": 0.775077760219574,
        "disgust": 0.9845525026321411,
        "joy": 0.09944059699773788,
        "anger": 0.35847562551498413,
        "surprise": 0.04079458490014076,
        "sadness": 0.12923076748847961,
        "fear": 0.03278418257832527
    }
}
```

**Notes:**
- The sentence splitter breaks text at the following characters: `;`, `:`, `.`, `?`, and `!`. 
- If a sentence is too short (<60 characters), it is concatenated with the preceding or following sentence.
- When sentences are concatenated, the original splitting character is replaced by a semicolon `;`.

**src.french.run.py**
Runs models (`emotions_detection_french`) trained on French text.
The models will process the entire text in `text_input.txt` in a single run.

`emotions_detection_french` returns results for 6 emotions, excluding the neutral state.
The results are saved in `response\response_emotion_french.json`.

Example:
```json
{
    "tristesse": 0.29552802443504333,
    "joie": 0.4873672425746918,
    "dégoût": 0.06737948209047318,
    "colère": 0.08569731563329697,
    "peur": 0.04895404353737831,
    "surprise": 0.015073847956955433
}
```

**src.french.run_per_sentence.py**

This runner splits the text in `text_input.txt` into sentences using the same rules as the English version. Each sentence is analyzed individually. Results for each sentence are saved in `response\response_per_sentence_emotion_french.json`. A statistical summary is saved in `response\stats_response_per_sentence_emotion_french.json`.


**src.multilingual.run.py**

An alternative option using a decoder model (`Gemma-4-E2B-it`) is provided for the following reasons:
- It can leverage reasoning and follow complex instructions, such as those required for multi-emotion sentiment analysis.
- It is better at processing long texts.
- It can be instructed to return emotion intensities rather than emotion probabilities.
- It can be prompted with specific emotions or even emotion definitions to better capture nuances.

While lightweight for a decoder model, `Gemma-4-E2B-it` is significantly larger than encoder models and may take several minutes to run when reasoning is enabled. The model runs on the CPU to ensure compatibility across all hardware.

The reasoning output is saved in `response\reasoning_Gemma_4_E2B.txt`.
The final output with emotion intensities is saved in `response\response_Gemma_4_E2B.json`.

**Notes:**
- Gemma 4 is instructed to return emotion intensities between 0 (lowest) and 100 (highest). For comparability with other models, these values are divided by 100 during post-processing so that they range between 0 and 1.
- Gemma 4 returns emotion intensities, whereas the other models return emotion probabilities.


# CUSTOM PARAMETERS

Customizable parameters are located in `src/config.py`.


# RESET

If you make any modifications to the code that you do not wish to keep (e.g., if the code becomes broken), you can reset the repository to its default state using the command:
```bash
git pull
```

# GUI

A GUI (Graphical User Interface) is provided and can be launched with the command:
```bash
python -m streamlit run src/gui.py
```

Functionalities:
- **Language**: select "en" to process english text and "fr" to process french text.
- **Number of emotions**: (available only if "en" is selected): in english, two models are available, one with 7 categories, the other with 28 categories. Choose the number corresponding to the model you want to use.
- **Method**: select "Encoder" to use an encoder model (probability of emotions) and "Decoder" to use Gemma 4 (intensity of emotions)
- **Analysis per sentence**: if True, runs the analysis on each sentence individually. Else, runs the analysis on the entire text globally.
- **Select Elements**: (available only if "Decoder" is selected) a list of elements, with the possibility to select a few or to select all, and to add new elements manually.
- **Optional emotion definitions**: (available only if "Decoder" is selected) a text area to enter definitions of emotions. It is recommended to add a linebreak between definitions.

