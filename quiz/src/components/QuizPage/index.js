import React, { useEffect, useState, useRef } from "react";
import { connect } from "react-redux";
import { Prompt } from "react-router-dom";
import { QuestoesCounter } from "./styles";
import moment from 'moment'
// import acertouAudio from '../../assets/audio/acertou-audio.mp3'
// import errouAudio from '../../assets/audio/errou-audio.mp3'
// import UIfx from 'uifx'
import {
  getQuestoes,
  acertouQuestao,
  errouQuestao,
  setTempo,
} from "../../actions/quiz";
import Navbar from "../Navbar";
import Quiz from "../Quiz";
import QuizFooter from "../QuizFooter";

function QuizPage(props) {
  const { quiz, setTempo, getQuestoes, acertouQuestao, errouQuestao } = props;
  // const acertouSound = new UIfx({ asset: acertouAudio })
  // const errouSound = new UIfx({ asset: errouAudio })
  let questaoAtual = quiz.questoes[quiz.questaoAtualIndice];

  const initialState = {
    alternativaSelecionada: null,
    timestampInicio: null,
    respondido: false,
    acertou: null,
  };

  const [state, setState] = useState(initialState);
  const { alternativaSelecionada } = state;

  useEffect(() => {
    async function loadPage() {
      const { modulo, nivel } = props.match.params;
      getQuestoes(modulo, nivel);
      setState({
        ...state,
        // timestampInicio: new Date().toLocaleTimeString(),
        timestampInicio: moment().format('HH:mm:ss.SSS'),
      });
    }

    loadPage();
  }, []);

  useEffect(() => {
    async function onNextQuestion() {
      setState({
        ...initialState,
        // timestampInicio: new Date().toLocaleTimeString(),
        timestampInicio: moment().format('HH:mm:ss.SSS'),
      });
    }

    onNextQuestion();
  }, [quiz.questaoAtualIndice]);

  useEffect(() => {
    if (state.respondido && state.acertou) {
      // acertouSound.play()
      acertouQuestao();
    } else if (state.respondido && state.acertou === false) {
      // errouSound.play()
      errouQuestao();
    }
  }, [state.respondido]);

  const selecionarAlternativa = (alternativa) => {
    setState({
      ...state,
      alternativaSelecionada: alternativa,
    });
  };

  const setParentState = (newState) => {
    setState({
      ...state,
      ...newState,
    });
  };

  // evita que o usuário recarregue a página sem confirmação
  const didMountRef = useRef(false);
  useEffect(() => {
    if (didMountRef.current) {
      if (!quiz.quizFinalizado) {
        window.onbeforeunload = () => true;
      } else {
        window.onbeforeunload = undefined;
      }
    } else didMountRef.current = true;
  });

  // if loading
  if (!questaoAtual && quiz.emProgresso) {
    return <h5>Carregando...</h5>;
  }

  return (
    !quiz.quizFinalizado && (
      <>
        <Prompt
          when={!quiz.quizFinalizado}
          message="Se sair agora perderá seu progresso no quiz, deseja continuar?"
        />
        <QuestoesCounter title="Progresso">
          {quiz.questaoAtualIndice + 1}/{quiz.questoes.length}
        </QuestoesCounter>
        <Navbar
          progresso={quiz.progresso}
          questaoAtualIndice={quiz.questaoAtualIndice}
          qtdQuestoes={quiz.questoes.length}
        />
        <Quiz
          questao={questaoAtual}
          selecionarAlternativa={selecionarAlternativa}
          alternativaSelecionada={alternativaSelecionada}
          respondido={state.respondido}
        />
        <QuizFooter
          questaoAtual={questaoAtual}
          selecionarAlternativa={selecionarAlternativa}
          setParentState={setParentState}
          {...state}
        />
      </>
    )
  );
}

const mapStateToProps = (state) => ({
  quiz: state.quizReducer.quiz,
});

export default connect(mapStateToProps, {
  setTempo,
  getQuestoes,
  acertouQuestao,
  errouQuestao,
})(QuizPage);
