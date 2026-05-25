data = [
    {
        "sentence": "example 1",
        "emotions": {
            "sadness": 0.98,
            "anger": 0.01,
            "disgust": 0.01,
            "neutral": 0.0,
            "joy": 0.0,
            "surprise": 0.0,
            "fear": 0.0
        }
    },
    {
        "sentence": "example 2",
        "emotions": {
            "sadness": 0.94,
            "anger": 0.01,
            "disgust": 0.0,
            "neutral": 0.03,
            "joy": 0.0,
            "surprise": 0.01,
            "fear": 0.01
        }
    }
]

def test_calculate_average():
    from common import calculate_average
    output = calculate_average(data)
    print(output)
    correct = {
        "sadness": 0.96,
        "anger": 0.01,
        "disgust": 0.005,
        "neutral": 0.015,
        "joy": 0.0,
        "surprise": 0.005,
        "fear": 0.005
    }
    for k, v in output.items():
        assert v == correct[k]
    
    
def test_calculate_min():
    from common import calculate_min
    output = calculate_min(data)
    print(output)
    correct = {
        "sadness": 0.94,
        "anger": 0.01,
        "disgust": 0.0,
        "neutral": 0.0,
        "joy": 0.0,
        "surprise": 0.0,
        "fear": 0.0
    }
    for k, v in output.items():
        assert v == correct[k]
    

def test_calculate_max():
    from common import calculate_max
    output = calculate_max(data)
    print(output)
    correct = {
        "sadness": 0.98,
        "anger": 0.01,
        "disgust": 0.01,
        "neutral": 0.03,
        "joy": 0.0,
        "surprise": 0.01,
        "fear": 0.01
    }
    for k, v in output.items():
        assert v == correct[k]