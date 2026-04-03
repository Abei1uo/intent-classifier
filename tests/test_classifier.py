import json
import pytest
from app.classifier import IntentClassifier


@pytest.fixture(scope="module")
def classifier():
    return IntentClassifier()


def test_cases(classifier):
    with open("tests/fixtures/test_cases.json") as f:
        cases = json.load(f)

    for case in cases:
        result = classifier.classify(case["text"], threshold=0.5)
        assert result["intent"] == case["expected"], \
            f"text={case['text']!r} expected={case['expected']} got={result['intent']} score={result['score']:.3f}"