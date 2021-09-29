import {
  GET_QUIZ_INFO,
  GET_ALUNO,
  GET_QUESTOES,
  START_QUIZ,
  SET_TEMPO,
  ACERTOU_QUESTAO,
  ERROU_QUESTAO,
  NEXT_QUESTION,
  FINALIZAR_QUIZ,
  GET_RESULTADO,
} from "../actions/types";

const initialState = {
  turma: {},
  modulo: {},
  aluno: null,
  quiz: {
    quizFinalizado: false,
    emProgresso: false,
    // podeVoltar: false,
    // podeContinuar: false,

    questoes: [],

    questaoAtualIndice: null,
    progresso: 0,

    tempo: null,
    questoesCorretas: 0,
    pontos: 0,
    tempoMedioPorQuestao: null,
    proximoNivelBloqueado: null,
    aprovadoNoQuiz: null,
    subiuDeNivel: null,
    nivelAlunoModulo: null,
    linksDeEstudo: [],
    mediaMinDeAprovacao: null
  },
};

export default function (state = initialState, action) {
  switch (action.type) {
    case GET_QUIZ_INFO:
      return {
        ...state,
        turma: action.payload.turma,
        modulo: action.payload.modulo,
        quiz: {
          ...state.quiz,
          mediaMinDeAprovacao: action.payload.media_min_de_aprovacao
        }
      };

    case GET_ALUNO:
      return {
        ...state,
        aluno: action.payload,
      };

    case GET_QUESTOES:
      return {
        ...state,
        quiz: {
          ...state.quiz,
          questoes: action.payload,
          progresso: (1 / action.payload.length) * 100,
        },
      };

    case START_QUIZ:
      return {
        ...state,
        quiz: {
          ...state.quiz,
          emProgresso: true,
          questaoAtualIndice: 0,
        },
      };

    case SET_TEMPO:
      let newState = {
        ...state,
        quiz: {
          ...state.quiz,
          tempo: action.payload,
        },
      };
      console.log(action.payload);
      return newState;

    // remover --
    case ACERTOU_QUESTAO:
      return {
        ...state,
        quiz: {
          ...state.quiz,
          questoesCorretas: state.quiz.questoesCorretas + 1,
        },
      };

    case ERROU_QUESTAO:
      return {
        ...state,
        quiz: {
          ...state.quiz,
          questoesIncorretas: state.quiz.questoesIncorretas + 1,
        },
      };
    // remover --

    case NEXT_QUESTION:
      // let progresso = ((state.quiz.questaoAtualIndice + 1) / state.quiz.questoes.length) * 100
      return {
        ...state,
        quiz: {
          ...state.quiz,
          progresso:
            ((state.quiz.questaoAtualIndice + 2) / state.quiz.questoes.length) *
            100,
          questaoAtualIndice: state.quiz.questaoAtualIndice + 1,
        },
      };

    case FINALIZAR_QUIZ:
      return {
        ...state,
        quiz: {
          ...initialState.quiz,
          // progresso:
          //   ((state.quiz.questaoAtualIndice + 1) / state.quiz.questoes.length) *
          //   100,
          quizFinalizado: true,
        },
      };

    case GET_RESULTADO:
      return {
        ...state,
        quiz: {
          ...state.quiz,
          ...action.payload,
        },
      };

    default:
      return state;
  }
}
