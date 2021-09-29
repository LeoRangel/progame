import styled from "styled-components";
import { constants } from "../../styles/constants";

export const Container = styled.div`
  width: 100%;
  margin-top: ${constants.heightQuestoesFixosTopSoma};
  margin-bottom: ${constants.footerQuestoesHeight};
  padding: 50px 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: black;

  @media (max-width: 768px) {
    margin-bottom: ${constants.footerQuestoesHeightTelaP};
    margin-bottom: calc(${constants.footerQuestoesHeightTelaP} + 55px);
    padding: 20px;
  }
`;

export const QuestaoContainer = styled.div`
  width: 100%;
  max-width: ${constants.larguraMaxContainer};
  display: flex;
  flex-flow: row wrap;
`;

export const AlternativasContainer = styled.div`
  display: flex;
  flex-flow: column;
  justify-content: flex-start;
  align-items: flex-start;
  flex: 0 0 40%;
  padding: 2px 25px;
  overflow-y: auto;

  @media (min-width: 768px) {
    max-height: calc(
      100vh - ${constants.footerQuestoesHeight} -
        ${constants.heightQuestoesFixosTopSoma} - 100px
    );
  }

  @media (max-width: 768px) {
    flex: 0 0 100%;
    padding: 2px;
  }
`;
