import styled from "styled-components";
import { constants } from "../../styles/constants";

export const Container = styled.div`
  width: 100%;
  min-height: ${constants.footerQuestoesHeight};
  padding: 20px 10px;
  border-top: ${constants.borda1};
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  z-index: 8 !important;
  color: white;
  position: fixed;
  bottom: 0;
  right: 0;
  left: 0;
  transition: background-color linear 0.5s;

  ${(props) => {
    if (!props.respondido) {
      return `
        background-color: #fff;
      `;
    } else if (props.respondido && props.correto) {
      return `
          background-color: ${constants.corNivel1};
          z-index: 15 !important;
        `;
      } else if (props.respondido && !props.correto) {
        return `
          background-color: ${constants.corNivel4};
          z-index: 15 !important;
      `;
    }
  }}

  @media (max-width: 768px) {
    min-height: ${constants.footerQuestoesHeightTelaP};
    padding: 20px;
  }
`;

export const FooterWrapper = styled.div`
  width: 100%;
  max-width: ${constants.larguraMaxContainer};
  display: flex;
  flex-direction: row;
  justify-content: space-between;

  @media (min-width: 768px) {
    padding-right: 25px;
  }
  @media (max-width: 768px) {
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
  }
`;

export const Feedback = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  transition: width 0.5s linear, height 0.5s linear;

  & .correto,
  & .incorreto {
    display: flex;
    flex-direction: row;
    align-items: center;
    color: white;
  }

  & .icone {
    margin-right: 10px;
  }

  & .infos {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  & h5 {
    font-size: 1.5em;
    font-weight: bold;
    margin-bottom: 2px;
  }

  & span {
    font-size: 0.9em;
  }

  @media (max-width: 768px) {
    & .correto,
    & .incorreto {
      margin-bottom: 20px;
    }
  }
`;

export const BotaoContainer = styled.div`
  display: flex;
  align-items: center;

  & button {
    transition-property: background-color, color;
    transition-timing-function: ease-in-out;
    transition-duration: 0.2s;

  }

  @media (max-width: 768px) {
    width: 100% !important;
  }

`;

export const Confirmar = styled.button`
  text-decoration: none;
  padding: 13px 26px;
  color: white;
  border: none;
  outline: none !important;
  border-radius: ${constants.botaoBordaRaio};
  background-color: ${(props) =>
    props.disabled ? constants.corPrimariaDisabled : constants.corPrimaria};

  &:hover {
    background-color: ${(props) =>
      props.disabled ? constants.corPrimariaDisabled : constants.corPrimariaHover};
  }

  &.botao-bloqueado {
    color: ${constants.botaoBloqueadoCor};
    background: none;
    border: ${constants.botaoBloqueadoBorda};
    pointer-events: none;
    cursor: default;

    &:hover {
      background-color: white;
    }
  }

  @media (max-width: 768px) {
    width: 100% !important;
  }
`;

export const Continuar = styled.button`
  text-decoration: none;
  padding: 13px 26px;
  color: white;
  outline: none !important;
  border: 1px solid white;
  border-radius: ${constants.botaoBordaRaio};
  background: transparent;

  @media (max-width: 768px) {
    width: 100% !important;
  }
`;
