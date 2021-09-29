import styled from "styled-components";
import { constants } from "../../styles/constants";
// import { Link } from "react-router-dom";

export const Container = styled.div`
  margin-top: ${constants.navbarHeight};
  height: calc(
    100vh - ${constants.navbarHeight}
  );
  display: flex;
  align-items: center;
  justify-content: center;
`;

export const Card = styled.div`
  padding: 25px;
  max-width: 470px;
  border-radius: ${constants.bordaRaioPadrao} !important;

  @media (max-width: 768px) {
    width: 100%;
  }
`;

export const ButtonContainer = styled.div`
  margin-top: 30px;
  width: 100%;
  display: flex;
  flex-direction: column;
`;

export const PlayButton = styled.button`
  border-radius: ${constants.botaoBordaRaio};
  background-color: ${constants.corPrimaria};
  color: #fff !important;
  transition: background-color 0.2s ease-in-out;
  padding: 15px;
  display: inline-block;
  /* text-decoration: none !important; */
  border: none;
  outline: none;
  text-align: center;
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: .25rem;

  &:hover {
    background-color: ${constants.corPrimariaHover};
  }

  &:active,
  &:focus {
    background-color: ${constants.corPrimariaHover};
  }
`;

export const VoltarButton = styled.a`
  border-radius: ${constants.botaoBordaRaio};
  border: ${constants.borda1};
  color: #000 !important;
  transition: background-color 0.2s ease-in-out;
  padding: 15px;
  display: inline-block;
  text-decoration: none !important;
  text-align: center;
  cursor: pointer;
  text-transform: uppercase;
  letter-spacing: .25rem;

  &:hover {
    background-color: ${constants.cinza1};
  }
`;
