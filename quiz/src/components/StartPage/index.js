import React, { Component } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { getAluno, getQuizInfo, startQuiz } from "../../actions/quiz";
import Navbar from "../Navbar";

import {
  Container,
  Card,
  ButtonContainer,
  PlayButton,
  VoltarButton,
} from "./styles";

class StartPage extends Component {
  static propTypes = {
    turma: PropTypes.object.isRequired,
    modulo: PropTypes.object.isRequired,
    questoes: PropTypes.array.isRequired,
  };

  componentDidMount() {
    this.props.getAluno();
    this.props.getQuizInfo(this.props.match.params.modulo, this.props.match.params.nivel);
  }

  render() {
    const { turma, modulo, startQuiz, history, aluno, mediaMinDeAprovacao } = this.props;
    const params = this.props.match.params;
    const voltarUrl = `/aluno/modulo/${params.modulo}/`;

    async function handleStart() {
      await startQuiz();
      history.push(`/quiz/${params.modulo}/${params.nivel}/play/`);
    }

    return (
      (aluno && Object.keys(turma).length !== 0) && (
        <>
          <Navbar />
          <Container className="container">
            <Card className="card">
              <h3 className="mb-4 font-weight-bold">Está preparado?</h3>
              <div>
                Você está iniciando o quiz <strong>nível {params.nivel}</strong>{" "}
                do módulo
                <strong> {modulo.nome}</strong>, da turma{" "}
                <strong>{turma.nome}</strong>.
                Obtenha, no mínimo, <strong>{mediaMinDeAprovacao}</strong> de acertos para ser aprovado.
              </div>

              <div className="mt-3 text-muted">
                <small>
                  Observação: os pontos do quiz são calculados com base no tempo de resposta e
                  número de tentativas realizadas e não influenciam na sua aprovação no quiz. <a href="/ajuda/quizzes/#item-4" target="_blank" >Saber mais sobre as pontuações?</a>
                </small>
              </div>
              <ButtonContainer>
                <PlayButton onClick={handleStart}>PLAY</PlayButton>
                {/* <VoltarButton href={voltarUrl}>Voltar</VoltarButton> */}
              </ButtonContainer>
            </Card>
          </Container>
        </>
      )
    );
  }
}

const mapStateToProps = (state) => ({
  turma: state.quizReducer.turma,
  modulo: state.quizReducer.modulo,
  questoes: state.quizReducer.quiz.questoes,
  emProgresso: state.quizReducer.quiz.emProgresso,
  aluno: state.quizReducer.aluno,
  mediaMinDeAprovacao: state.quizReducer.quiz.mediaMinDeAprovacao
});

export default connect(mapStateToProps, {
  getAluno,
  getQuizInfo,
  startQuiz,
})(StartPage);
