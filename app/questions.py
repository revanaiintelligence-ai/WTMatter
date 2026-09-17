from typing import List

from .models import WTMQuestion


class WTMQuestionManager:
    """
    Administrador de preguntas de WTM.

    Su función es construir preguntas normalizadas
    a partir de información que falta o necesita aclaración.

    No realiza diagnóstico de BINAH.
    """

    def build_basic_questions(
        self,
        context: bool,
        objective: bool,
        situation: bool,
    ) -> List[WTMQuestion]:
        """
        Genera las preguntas estructurales iniciales de WTM.
        """

        questions: List[WTMQuestion] = []

        if not context:
            questions.append(
                self.create_question(
                    question_id="context",
                    text="¿En qué contexto ocurre la situación que quieres analizar?",
                    question_type="MISSING_INFORMATION",
                    target="context",
                )
            )

        if not objective:
            questions.append(
                self.create_question(
                    question_id="objective",
                    text="¿Qué quieres lograr o cambiar con respecto a esta situación?",
                    question_type="OBJECTIVE",
                    target="objective",
                )
            )

        if not situation:
            questions.append(
                self.create_question(
                    question_id="situation",
                    text="¿Qué está ocurriendo actualmente y por qué consideras que necesita atención?",
                    question_type="CLARIFICATION",
                    target="situation",
                )
            )

        return questions

    @staticmethod
    def create_question(
        question_id: str,
        text: str,
        question_type: str,
        target: str,
        required: bool = True,
    ) -> WTMQuestion:
        """
        Construye una pregunta WTM normalizada.
        """

        return WTMQuestion(
            id=f"Q_{question_id}",
            text=text,
            type=question_type,
            target=target,
            required=required,
            answered=False,
        )