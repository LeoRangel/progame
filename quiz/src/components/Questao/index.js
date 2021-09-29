import React from "react";

import {
  Container,
  Pergunta,
  HeaderPergunta,
  DescricaoPergunta,
} from "./styles";

export default function Questao({ questao }) {
  return (
    <Container>
      <Pergunta>
        <HeaderPergunta>{questao.sentenca}</HeaderPergunta>
        {questao.descricao && (
          <DescricaoPergunta
            dangerouslySetInnerHTML={{ __html: questao.descricao }}
          />
          // <DescricaoPergunta dangerouslySetInnerHTML={questao.descricao} >{questao.descricao}</DescricaoPergunta>
        )}
      </Pergunta>
    </Container>
  );
}
