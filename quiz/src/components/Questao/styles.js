import styled from "styled-components";
import { constants } from "../../styles/constants";

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  flex: 0 0 60%;
  overflow-y: auto;
  
  background-color: rgb(0, 0, 0, 0.03);
  padding: 25px;
  
  @media (max-width: 768px) {
    flex: 0 0 100% !important;
    margin-right: 0;
    margin-bottom: 20px;
  }
  @media (min-width: 768px) {
    height: calc(
      100vh - ${constants.footerQuestoesHeight} -
        ${constants.heightQuestoesFixosTopSoma} - 100px
    );
  }
`;

export const Pergunta = styled.div`
  width: 100%;
  max-width: ${constants.larguraMaxContainer};
  display: flex;
  flex-flow: row wrap;
`;

export const HeaderPergunta = styled.div`
  font-size: 1.4em;
  font-weight: bold;
  margin-bottom: 30px;
`;

export const DescricaoPergunta = styled.div``;
