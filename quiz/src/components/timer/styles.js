import styled from "styled-components";
import { constants } from "../../styles/constants";

export const Container = styled.div`
  width: 100%;
  height: 0;
  // min-height: ${constants.footerQuestoesHeight};
  // padding: 20px 10px;
  padding: 0 10px;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  z-index: 15 !important;
  color: black;
  position: fixed;
  bottom: 0;
  right: 0;
  left: 0;

  @media (max-width: 768px) {
    // min-height: ${constants.footerQuestoesHeightTelaP};
    padding-left: 20px;
    padding-right: 20px;
  }
`;

export const FooterWrapper = styled.div`
  width: 100%;
  max-width: ${constants.larguraMaxContainer};
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  position: relative;
  
  // @media (min-width: 768px) {
  //   padding-right: 25px;
  // }
  // @media (max-width: 768px) {
  //   flex-direction: column;
  //   align-items: flex-start;
  //   justify-content: center;
  // }
`;


export const Contador = styled.div`
  position: absolute;
  max-width: 150px;
  left: 0;
  bottom: calc( ${constants.footerQuestoesHeightTelaP} );
  transform: translate(0%, 110%);

  & .numero {
    font-size: 20px;
    padding: 10px 20px;
    // min-width: 50px;
    // border: ${constants.borda1};
    display: flex;
    text-align: center;
    justify-content: center;
    border-radius: 15px;
  }
  & .nao-pontuar {
    font-size: 10px;
    padding: 10px;
    // border: ${constants.borda1};
    display: flex;
    text-align: center;
    border-radius: 15px;
  }

  @media (max-width: 768px) {
    transform: unset;
    left: unset;
    right: 0;
    bottom: 110px;
    // box-shadow: ${constants.sombra1};

    & .nao-pontuar {
      text-align: right;
    }
  }
`;

