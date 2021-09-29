import { RESPONDER_QUESTAO } from "../actions/types";

const initialState = {
  questoesRespondidas: [
    // {
    //   id: 1,
    //   hora_inicio: "18:00:00",
    //   hora_fim: "20:01:44.993612",
    //   questao: 1,
    //   alternativa: 1,
    //   aluno: 1,
    // },
  ],
};

export default function (state = initialState, action) {
  switch (action.type) {
    case RESPONDER_QUESTAO:
      return {
        ...state,
        questoesRespondidas: [...state.questoesRespondidas, action.payload],
      };

    default:
      return state;
  }
}
