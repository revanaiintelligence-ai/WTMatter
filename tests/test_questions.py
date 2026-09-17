from app.questions import WTMQuestionManager


def test_build_basic_questions_when_information_is_missing():
    manager = WTMQuestionManager()

    questions = manager.build_basic_questions(
        context=False,
        objective=False,
        situation=False,
    )

    assert len(questions) == 3

    question_ids = [
        question.id
        for question in questions
    ]

    assert "Q_context" in question_ids
    assert "Q_objective" in question_ids
    assert "Q_situation" in question_ids


def test_build_basic_questions_when_information_is_complete():
    manager = WTMQuestionManager()

    questions = manager.build_basic_questions(
        context=True,
        objective=True,
        situation=True,
    )

    assert questions == []


def test_create_question():
    manager = WTMQuestionManager()

    question = manager.create_question(
        question_id="test",
        text="Pregunta de prueba",
        question_type="CLARIFICATION",
        target="situation",
    )

    assert question.id == "Q_test"
    assert question.text == "Pregunta de prueba"
    assert question.type == "CLARIFICATION"
    assert question.target == "situation"
    assert question.required is True
    assert question.answered is False