import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

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
} from "./types";

// GET QUIZ INFO
export const getQuizInfo = (modulo_uuid, nivel) => (dispatch) => {
  axios
    .get(`/api/quiz/${modulo_uuid}/${nivel}/`)
    .then((res) => {
      dispatch({
        type: GET_QUIZ_INFO,
        payload: res.data,
      });
    })
    .catch((err) => {
      console.log(err);
    });
};

// GET ALUNO
export const getAluno = () => (dispatch) => {
  axios
    .get(`/api/aluno/`)
    .then((res) => {
      dispatch({
        type: GET_ALUNO,
        payload: res.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: GET_ALUNO,
        payload: null,
      });
    });
};

// GET QUESTÕES
export const getQuestoes = (modulo_uuid, nivel) => (dispatch) => {
  axios
    .get(`/api/questao/modulo/${modulo_uuid}/${nivel}/`)
    .then((res) => {
      dispatch({
        type: GET_QUESTOES,
        payload: res.data,
      });
    })
    .catch((err) => {
      console.log(err);
    });
};

// START QUIZ
export const startQuiz = () => (dispatch) => {
  dispatch({
    type: START_QUIZ,
  });
};

export const setTempo = (tempo) => (dispatch) => {
  dispatch({
    type: SET_TEMPO,
    payload: tempo
  })
}

// ACERTOU QUESTÃO
export const acertouQuestao = () => (dispatch) => {
  dispatch({
    type: ACERTOU_QUESTAO,
  });
};

// ERROU QUESTÃO
export const errouQuestao = () => (dispatch) => {
  dispatch({
    type: ERROU_QUESTAO,
  });
};

// PRÓXIMA QUESTÃO
export const nextQuestion = () => (dispatch) => {
  dispatch({
    type: NEXT_QUESTION,
  });
};

// FINALIZAR QUIZ
export const finalizarQuiz = () => (dispatch) => {
  dispatch({
    type: FINALIZAR_QUIZ,
  });
};

// GET RESULTADO
export const getResultado = (data) => (dispatch) => {
  axios
    .post(`/api/resultado/`, data)
    .then((res) => {
      dispatch({
        type: GET_RESULTADO,
        payload: res.data,
      });
    })
    .catch((err) => {
      console.error(err);
    });
};
