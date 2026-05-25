# INSTALLATION

1. Install python (preferably, python 3.12) (https://www.python.org/downloads/release/python-3120/)

2. Install Git (https://git-scm.com/install/)

3. Create a project folder

4. Open powershell

5. In powershell, go in the folder where you want to add the project repository
```bash
cd C:\Users\myusername\Documents\pick_a_repo
```

6. Clone the project repository
```bash
git clone https://github.com/fabienpv/sentiment_analysis.git
```

7. Move into the project repository
```bash
cd sentiment_analysis
```

8. Create a virtual environment (recommended name: .venv)
```bash
python -m venv .venv
```

9. Download the requirements (the libraries needed to run the scripts). It's going to take a few minutes.
```bash
pip install -r requirements.txt
```

10. Clone the model repositories from Hugging Face. It's going to take a few minutes for each download.
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

At the end of the installation, the structure of the project repository should be:

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


# HOW TO USE

The runable python scripts are:

src.english.run.py
src.english.run_per_sentence.py
src.french.run.py
src.french.run_per_sentence.py
src.multilingual.run.py
src.gui.py

1. Open powershell or cmd

2. Go in the project directory. 
```bash
cd C:\Users\myusername\Documents\pick_a_repo\sentiment_analysis
```

3. If you want to run the gui:
```bash
python -m streamlit run src/gui.py
```

if you want to run the run*.py:

Start by writting the text you want to process in text_input.txt.
Then, run the file with python -m
example:
```bash
python -m src.french.run
```

The result will be displayed in the terminal (cmd or powershell window)

# RUNNERS

**src.english.run.py**
Runs decoder models (roberta-base-go_emotions and emotion-english-distilroberta-base) trained with english text.
The models will process the text written in __text_input.txt__ in one single run (one analysis on the full text).

emotion-english-distilroberta-base will return the result for 6 emotions + the neutral state.
The output will be saved in __response\response_emotion_english_distilroberta.json__
example: 
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

roberta-base-go_emotions will return the result for 27 emotions + the neutral state.
The output will be saved in __response\response_roberta_go_emotions.json__
example: 
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

Notes: 
- the models give emotion probabilities such that the sum of all score should be 1 (or approximately 1 with roberta-base-go_emotions). 
- the models were probably trained with relatively short texts
- the models were probably trained to the text in 1 single class. Therefore, they might overestimate the probability of the main emotion and underestimate the probability of all other emotions
- the scores are emotion probabilities, not emotion intensities

**src.english.run_per_sentence.py**

Since the models might have been trained with rather short texts, it was decided to create another runner (this one) which would split the text into sentences and run the sentiment analysis on each sentence individually.
The result for each sentence is saved in __response\response_per_sentence__emotion_english.json__
A summary of the results containing the number of sentences, the average scores per emotion, the max score per emotion and the min score per emotion across all sentences is saved in __response\stats_response_per_sentence__emotion_english.json__.

example of result per sentence:
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
    },
    ...
]
```

example of statistical summary:
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

Notes:
- The sentence splitter splits the text on each of the following character: ";", ":", ".", "?", "!". 
- If a sentence is too short (<60 characters), it is concatenated with the previous or next sentence.
- When sentences are concatenated, the splitting character (lost during the splitting operation) is replaced by a semicolon ";".


**src.french.run.py**
Runs decoder models (emotions_detection_french) trained with english text.
The models will process the text written in __text_input.txt__ in one single run (one analysis on the full text).

emotions_detection_french will return the result for 6 emotions without neutral state.
The results are saved in __response\response_emotion_french.json__

example:
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

Notes:
- fewer models exists for emotion analysis in french than in english, and not all models contain disgust
- a for the english models, this one returns the probability of each emotion. 


**src.french.run_per_sentence.py**

This runner splits the text in __text_input.txt__ into sentences. The sentence splitter is the same than in english, and the same splitting rules apply. Each sentence is analyze individually by the model. The results for each individual sentences are saved in __response\response_per_sentence__emotion_french.json__. A summary of the results containing the number of sentences, the average scores per emotion, the max score per emotion and the min score per emotion across all sentences is saved in __response\stats_response_per_sentence__emotion_french.json__.


**src.multilingual.run.py**

An alternative option using a decoder model (Gemma-4-E2B-it) is provided for the following reasons:
- it can leverage reasoning and follow complex instructions such as those required for multi-emotion sentiment analysis
- it is better at processing long texts
- we can instruct it to return emotion intensities rather than emotion probabilities.
- we can instruct it with any emotion and even provide emotion definition to better capture nuances.

While lightweight for a decoder model, Gemma-4-E2B-it is considerably larger than encoder models and takes several minutes to run with the reasoning activated. The model runs on CPU to adapt all hardwares.

The reasoning output is saved in __response\reasoning_Gemma_4_E2B.txt__
The final output with emotion intensities is saved in __response\response_Gemma_4_E2B.json__.

Notes:
- Gemma 4 is instructed to return emotions intensities between 0 (lowest) and 100 (highest), but for comparability with the other models, the values are divided by 100 in post processing so that they range between 0 and 1.
- Gemma 4 returns emotion intensities whereas the other models return emotion probabilities.


# CUSTOM PARAMETERS

Customizable parameters are written inside src.config.py


# RESET

If you make any modification in the code that you don't wish too keep (e.g. because the code does not work anymore), you can reset the code to its default with the command:
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
- **Method**: select "Encoder" to use an encoder model (probability of emotions) and "Decoder" to use Gemma 4 (intensity of emotions)
- **Analysis per sentence**: if True, runs the analysis on each sentence individually. Else, runs the analysis on the entire text globally.
- **Select Elements**: (available only if "Decoded" is selected): 

