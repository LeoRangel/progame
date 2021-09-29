import React from "react";
import { Container } from "./styles";

function Alternativa(props) {
  const {
    alternativa,
    selecionarAlternativa,
    alternativaSelecionada,
    respondido,
  } = props;

  return (
    <Container
      selecionada={alternativa.id === alternativaSelecionada}
      incorreta={respondido && !alternativa.is_correta}
      correta={respondido && alternativa.is_correta}
      respondido={respondido}
      onClick={() => selecionarAlternativa(alternativa.id)}
    >
      {alternativa.nome}
    </Container>
  );
}

export default Alternativa;
