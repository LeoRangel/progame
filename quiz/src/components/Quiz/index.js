import React, { useEffect, useState } from "react";
import Questao from "../Questao";
import Alternativa from "../Alternativa";
import QuizFooter from "../QuizFooter";

import Timer from '../timer/index'

import { Container, QuestaoContainer, AlternativasContainer } from "./styles";

function Quiz(props) {
  const {
    questao,
    selecionarAlternativa,
    alternativaSelecionada,
    respondido,
  } = props;

  const [alternativas, setAlternativas] = useState([])

  useEffect(() => {
    async function shuffleAlternativas() {
      const shuffledAlternativas = await shuffleArray(questao.alternativas)
      setAlternativas(shuffledAlternativas)
    }

    shuffleAlternativas()
  }, [questao])

  function shuffleArray(array) {
    let i = array.length - 1;
    for (; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const temp = array[i];
      array[i] = array[j];
      array[j] = temp;
    }
    return array;
  }

  return (
    <>
      <Container>
        <QuestaoContainer>
          <Questao {...props} />
          <AlternativasContainer>
            {alternativas.map((alternativa) => (
              <Alternativa
                selecionarAlternativa={selecionarAlternativa}
                alternativaSelecionada={alternativaSelecionada}
                respondido={respondido}
                key={alternativa.id}
                alternativa={alternativa}
              />
            ))}
          </AlternativasContainer>
        </QuestaoContainer>
      </Container>
      
      <Timer
        startCount={questao.tempo_para_responder}
        questao={questao.id}
      />

      <QuizFooter />
    </>
  );
}

export default Quiz;
