import React, { useState, useEffect } from "react";
import { useHistory, useParams } from "react-router-dom";
import { connect } from "react-redux";
import { responderQuestao } from "../../actions/resposta";
import { nextQuestion, finalizarQuiz } from "../../actions/quiz";
import { FaCheckCircle, FaTimesCircle } from "react-icons/fa";
import moment from 'moment'

// import Acertou from '../../assets/sons/acertou2.ogg';
import Acertou from '../../assets/sons/acertou.mp3';
import Errou from '../../assets/sons/errou.ogg';

import {
  Container,
  FooterWrapper,
  Feedback,
  BotaoContainer,
  Confirmar,
  Continuar,
} from "./styles";


function QuizFooter(props) {

  const {
    questaoAtual,
    alternativaSelecionada,
    responderQuestao,
    setParentState,
    nextQuestion,
    timestampInicio,
    aluno,
    respondido,
    acertou,
    questoesRespondidas,
  } = props;

  const initialState = {
    alternativasCorretas:
      questaoAtual &&
      questaoAtual.alternativas.filter((alternativa) => alternativa.is_correta),
  };

  const history = useHistory();
  const { modulo, nivel } = useParams();
  const [state, setState] = useState(initialState);

  useEffect(() => {
    setState(initialState);
  }, [questaoAtual]);

  // REFATORAR
  const renderFeedback = (acertou) => {
    if (acertou) {
      return (
        <div className="correto">
          <audio src={Acertou} autoPlay/>
          <div className="icone">
            <FaCheckCircle size={46} />
          </div>
          <div className="infos">
            <h5>Correto</h5>
            {questoesRespondidas[props.quiz.questaoAtualIndice] &&
              <span>+ {questoesRespondidas[props.quiz.questaoAtualIndice].pontos} pontos</span>
            }
          </div>
        </div>
      );
    }
    
    return (
      <div className="incorreto">
        <audio src={Errou} autoPlay/>
        <div className="icone">
          <FaTimesCircle size={46} />
        </div>
        <div className="infos">
          <h5>Errado</h5>
        </div>
      </div>
    );
  };

  const renderBotao = (respondido) => {
    if (respondido) {
      return <Continuar onClick={() => handleContinuar()}>Continuar</Continuar>;
    }
    return (
      <Confirmar
        onClick={() => handleResposta(alternativaSelecionada)}
        disabled={!alternativaSelecionada}
      >
        Confirmar
      </Confirmar>
    );
  };

  const handleResposta = (alternativaSelecionada) => {
    let acertou = state.alternativasCorretas.some(
      (alternativaCorreta) => alternativaCorreta.id === alternativaSelecionada
    );
    setParentState({
      respondido: true,
      acertou,
    });
    responderQuestao({
      hora_inicio: timestampInicio,
      hora_fim: moment().format('HH:mm:ss.SSS'),
      questao: questaoAtual.id,
      alternativa: alternativaSelecionada,
      aluno: aluno.id,
    });
  };

  async function handleContinuar() {
    if (props.quiz.questaoAtualIndice === props.quiz.questoes.length - 1) {
      await props.finalizarQuiz();
      history.push(`/quiz/${modulo}/${nivel}/resultado/`);
    } else {
      nextQuestion();
      setParentState({
        respondido: false,
        acertou: null,
      });
    }
  }

  return (
    <Container respondido={respondido} correto={acertou}>
      <FooterWrapper>
        <Feedback>{respondido && renderFeedback(acertou)}</Feedback>
        <BotaoContainer>{renderBotao(respondido)}</BotaoContainer>
      </FooterWrapper>
    </Container>
  );
}

const mapStateToProps = (state) => ({
  aluno: state.quizReducer.aluno,
  quiz: state.quizReducer.quiz,
  questoesRespondidas: state.respostaReducer.questoesRespondidas
});

export default connect(mapStateToProps, {
  responderQuestao,
  nextQuestion,
  finalizarQuiz,
})(QuizFooter);
