import { combineReducers } from "redux";
import quiz from "./quiz";
import resposta from "./resposta";

export default combineReducers({
  quizReducer: quiz,
  respostaReducer: resposta,
});
