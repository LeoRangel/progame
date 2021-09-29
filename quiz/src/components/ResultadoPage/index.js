import React, { useEffect, useState } from "react";
import {
  FaCheck,
  FaStopwatch,
  FaCalculator,
  FaArrowRight,
  FaTimes,
  FaUndo,
} from "react-icons/fa";
import { getResultado } from "../../actions/quiz";
import { getNomeNivel, getDescricaoNivel } from "../../utils";
import Swal from "sweetalert2";
import humanizeDuration from "humanize-duration";
import { useParams } from "react-router-dom";
import { connect } from "react-redux";
import "../../styles/css/lvlUp.css";
import {
  Container,
  Cards,
  Pontuacao,
  Ranking,
  Titulo,
  Nivel,
  Estudos,
  Footer,
  BotaoSecundario,
  BotaoPadrao,
} from "./styles";


// import SubiuNivel from '../../assets/sons/levelup.mp3';
import Perdeu from '../../assets/sons/perdeu.mp3';
import Ganhou from '../../assets/sons/ganhou.mp3';


function ResultadoPage(props) {
  const { aluno, quiz, questoesRespondidas, getResultado } = props;
  const { modulo, nivel } = useParams();
  const [linksEstudo, setLinksEstudo] = useState(null);

  useEffect(() => {
    getResultado({
      aluno: aluno.id,
      modulo: props.modulo.id,
      respostas: questoesRespondidas,
    });
  }, []);

  useEffect(() => {
    quiz.subiuDeNivel &&
      Swal.fire({
        title: "Você subiu de nível!",
        html: `
        <div class="d-flex w-100 position-relative justify-content-center mt-4 mb-5">
          <div id="initial-lvl" class="num-circle bgNivel${parseInt(quiz.nivelAlunoModulo) - 1}">
            <span>${parseInt(quiz.nivelAlunoModulo) - 1}</span>
          </div>
          <div class="line">
            <div class="progress"></div>
          </div>
          <div class="num-circle target-lvl bgNivel${quiz.nivelAlunoModulo}">
            ${quiz.nivelAlunoModulo}
          </div>
        </div>`,
        confirmButtonText: "Ok",
      });
    $(".progress").animate(
      {
        width: "152px",
      },
      1300,
      function () {
        $(".target-lvl").addClass("lvl-animate");
        $("#initial-lvl").fadeTo(500, 0, function () {
          $("#initial-lvl").css("visibility", "hidden");
        });
        $(".line").fadeTo(500, 0, function () {
          $(".line").css("visibility", "hidden");
        });
      }
    );
  }, [quiz.subiuDeNivel]);

  useEffect(() => {
    quiz.linksDeEstudo.length > 0 && setLinksEstudo(quiz.linksDeEstudo);
  }, [quiz.linksDeEstudo]);

  const renderBotao = () => {
    if (
      quiz.nivelAlunoModulo == nivel &&
      quiz.proximoNivelBloqueado === false
    ) {
      return (
        <BotaoPadrao
          href={`/quiz/${modulo}/${parseInt(quiz.nivelAlunoModulo) + 1}/`}
        >
          Quiz do próximo nível
          <FaArrowRight size={15} className="ml-2" />
        </BotaoPadrao>
      );
    } else if (quiz.subiuDeNivel === false) {
      return (
        <BotaoPadrao onClick={() => handleDoOver()}>
          Tentar novamente
          <FaUndo size={15} className="ml-2" />
        </BotaoPadrao>
      );
    }
  };

  function getInfoLinkEstudo(data) {
    if (data.nome) {
      return (
        <>
          <p title={data.nome}>{data.nome_trunc}</p>
          <span title={data.url}>{data.url_trunc}</span>
        </>
      );
    } else if (data.url) {
      return <p title={data.url}>{data.url_trunc}</p>;
    }
  }

  const renderLinksEstudo = () => {
    if (linksEstudo && linksEstudo.length > 0) {
      return (
        <ul className="links-estudo-list">
          {linksEstudo.map((link) => {
            return (
              <li key={link.id}>
                <a href={link.url} target="_blank">
                  <div
                    className="imagem"
                    style={{
                      backgroundImage: `url(/static/progame/img/open_in_new_tab.png)`,
                    }}
                  ></div>
                  <div className="info">{getInfoLinkEstudo(link)}</div>
                </a>
              </li>
            );
          })}
        </ul>
      );
    } else {
      <span className="text-muted">Nenhum link de estudo para esse quiz</span>;
    }
  };

  const handleDoOver = () => {
    Swal.fire({
      // icon: "warning",
      title: "Observação",
      html: `
            <div>
                <p>
                    Para assegurar-se de obter um bom desempenho no quiz,
                    recomenda-se que você tire antes as suas dúvidas estudando o assunto,
                    pois em cada nova tentativa feita
                    <a href="/ajuda/quizzes/#item-4" target="_blank">
                      o ganho de pontos é reduzido
                    </a>.
                </p>
            </div>
        `,
      confirmButtonText: "Continuar mesmo assim",
      showCancelButton: true,
      cancelButtonText: "Voltar para o módulo",
    }).then((res) => {
      if (res.value) {
        window.location.href = `/quiz/${modulo}/${nivel}/`;
      } else if (res.dismiss == "cancel") {
        window.location.href = `/aluno/modulo/${modulo}/`;
      }
    });
  };

  function tocarSom(aprovado) {
    if (aprovado == true) {
      return (
        <audio src={Ganhou} autoPlay/>
      );
    } else if (aprovado == false) {
      return (
        <audio src={Perdeu} autoPlay/>
      );
    }
  }

  return (
    quiz.quizFinalizado && (
      <Container className="bg-dark">
        { tocarSom(quiz.aprovadoNoQuiz) }
        <Cards>
          <Pontuacao>
            <div className="header">
              <span className="titulos">
                {quiz.aprovadoNoQuiz ? "Bom trabalho!" : "Não foi dessa vez..."}
              </span>
              <span className="subtitulos">
                {quiz.aprovadoNoQuiz
                  ? "Aqui está o seu resultado nesta atividade:"
                  : "Estude um pouco mais e tente novamente."}
              </span>
            </div>

            <div className="infos">
              <div className="questoes-acertadas">
                <div
                  className={`icone ${
                    quiz.aprovadoNoQuiz ? "text-success" : "text-danger"
                  }`}
                >
                  {quiz.aprovadoNoQuiz ? (
                    <FaCheck size={45} />
                  ) : (
                    <FaTimes size={45} />
                  )}
                </div>
                <div className="texto">
                  <span>Questões acertadas</span>
                  <span className="qtd">
                    {quiz.questoesCorretas.length}/{questoesRespondidas.length}
                  </span>
                </div>
              </div>

              <div className="tempo-medio">
                <div className="icone text-info">
                  <FaStopwatch size={45} />
                </div>
                <div className="texto">
                  <span>Tempo médio de resposta</span>
                  <span className="qtd">
                    {humanizeDuration(
                      parseFloat(quiz.tempoMedioPorQuestao) * 1000,
                      { language: "pt" }
                    )}
                  </span>
                </div>
              </div>
          
              <div className="pontos-ganhos">
                <div className="icone text-warning">
                  <FaCalculator size={45} />
                </div>
                <div className="texto">
                  <span>Total de pontos ganhos</span>
                  <span className="qtd">{quiz.pontos} pts</span>
                </div>
              </div>
            </div>
            <div className="alert alert-warning mb-0 mt-4" role="alert">
              {quiz.aprovadoNoQuiz ?
              `Você obteve ${quiz.mediaMinDeAprovacao} ou mais de acertos.`
              :
              `É necessário obter, no mínimo, ${quiz.mediaMinDeAprovacao} de acertos para ser aprovado no quiz.`
              }
              {/* {!quiz.aprovadoNoQuiz && `É necessário obter, no mínimo, ${quiz.mediaMinDeAprovacao} de acertos para ser aprovado no quiz.`} */}
            </div>
          </Pontuacao>

          <Ranking className="row">
            <div className="col-md-6 ranking">
              <Titulo>Rankign do módulo</Titulo>
              <div>
                <div className="posicao">
                  <h1>{quiz.posicaoAlunoModulo}ª</h1>
                  <span>Posição</span>
                </div>
              </div>
            </div>
            <div className="col-md-6 ranking">
              <Titulo>Ranking da turma</Titulo>
              <div className="">
                <div className="posicao">
                  <h1>{quiz.posicaoAlunoTurma}ª</h1>
                  <span>Posição</span>
                </div>
              </div>
            </div>
          </Ranking>

          <Nivel className={`bgNivel${quiz.nivelAlunoModulo}`}>
            <Titulo>Seu nível no módulo</Titulo>
            <div>
              <div className="nivel-oa">
                {/* <span>Seu nível</span> */}
                <h1>{quiz.nivelAlunoModulo}</h1>
                {/* <h1>{quiz.nivelAlunoModulo}/6</h1> */}
                <span>{getNomeNivel(parseInt(quiz.nivelAlunoModulo))}</span>
              </div>
            </div>
          </Nivel>

          <Estudos>
            <Titulo>Links de estudo que podem te ajudar</Titulo>
            <div className="links-wrapper">
              {linksEstudo && renderLinksEstudo()}
            </div>
          </Estudos>

          <Footer>
            {renderBotao()}
            <BotaoSecundario
              href={`/aluno/modulo/${modulo}/`}
              className="btn"
            >
              Voltar para o módulo
            </BotaoSecundario>
          </Footer>
        </Cards>
      </Container>
    )
  );
}

const mapStateToProps = (state) => ({
  modulo: state.quizReducer.modulo,
  aluno: state.quizReducer.aluno,
  quiz: state.quizReducer.quiz,
  questoesRespondidas: state.respostaReducer.questoesRespondidas,
});

export default connect(mapStateToProps, { getResultado })(ResultadoPage);
