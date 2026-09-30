def test_clean_json_block():

    from quiz_module import clean_json_block

    assert (
        clean_json_block(
            "```json\n[]\n```"
        )
        == "[]"
    )


def test_plain_json():

    from quiz_module import clean_json_block

    assert (
        clean_json_block("[]")
        == "[]"
    )


def test_main_application():

    import main

    assert (
        main.app.title
        == "EduGenie"
    )


def test_gemini_uses_fallback_model_on_503():

    from types import SimpleNamespace

    from config import GEMINI_FALLBACK_MODEL
    from gemini_client import _generate_content_with_fallback

    class TemporarilyUnavailable(Exception):
        code = 503

    class Models:

        def __init__(self):
            self.models = []

        def generate_content(self, model, contents, config):
            self.models.append(model)
            if len(self.models) == 1:
                raise TemporarilyUnavailable("503 UNAVAILABLE")
            return "answer"

    models = Models()
    client = SimpleNamespace(models=models)

    result = _generate_content_with_fallback(
        client,
        model="primary-model",
        contents="question",
        config=None
    )

    assert result == "answer"
    assert models.models == ["primary-model", GEMINI_FALLBACK_MODEL]


def test_supported_gemini_model_names():

    from config import GEMINI_MODEL, GEMINI_FALLBACK_MODEL

    assert GEMINI_MODEL.startswith("gemini-")
    assert "3.8" not in GEMINI_MODEL
    assert GEMINI_FALLBACK_MODEL.startswith("gemini-")
    assert "3.8" not in GEMINI_FALLBACK_MODEL


def test_generate_text_falls_back_when_gemini_fails(monkeypatch):

    import gemini_client

    monkeypatch.setattr(
        gemini_client,
        "get_client",
        lambda: object()
    )

    def raise_error(*args, **kwargs):
        raise RuntimeError("Gemini unavailable")

    monkeypatch.setattr(
        gemini_client,
        "_generate_content_with_fallback",
        raise_error
    )

    result = gemini_client.generate_text("What is photosynthesis?")

    assert "photosynthesis" in result.lower()