import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

import { RESPONDER_QUESTAO } from "./types";

// {
//     hora_inicio: "18:00:00",
//     questao: 1,
//     alternativa: 1,
//     aluno: 1,
// }

export const responderQuestao = (resposta) => (dispatch) => {
  axios
    .post(`/api/resposta/`, resposta)
    .then((res) => {
      dispatch({
        type: RESPONDER_QUESTAO,
        payload: res.data,
      });
    })
    .catch((err) => {
      console.log(err);
    });
};
