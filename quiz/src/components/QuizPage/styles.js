import styled from "styled-components";
import { constants } from "../../styles/constants";
import { Link } from "react-router-dom";

export const Container = styled.div`
  margin-top: ${constants.navbarHeight};
  height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
`;

export const QuestoesCounter = styled.div`
  position: absolute;
  top: 95px;
  left: 30px;
  color: rgba(0,0,0,0.1);
  font-size: 60px;
  font-weight: bold;
  display: block;
  cursor: default;

  @media (max-width: 1495px) {
    display: none;
  }
`;

export const Card = styled.div`
  padding: 30px;
  width: 60% !important;
`;

export const ButtonContainer = styled.div`
  margin-top: 30px;
  width: 100%;
  display: flex;
  flex-direction: column;
`;

export const PlayButton = styled(Link)`
  border-radius: ${constants.botaoBordaRaio};
  background-color: ${constants.corPrimaria};
  color: #fff !important;
  transition: background-color 0.2s ease-in-out;
  padding: 15px;
  display: inline-block;
  text-decoration: none !important;
  text-align: center;
  margin-bottom: 10px;
  font-weight: bold;

  &:hover {
    background-color: ${constants.corPrimariaHover};
  }

  &:active,
  &:focus {
    background-color: ${constants.corPrimariaHover};
  }
`;

export const VoltarButton = styled.a`
  border-radius: ${constants.bordaRaioPadrao};
  background-color: ${constants.cinza1};
  color: #000 !important;
  transition: background-color 0.2s ease-in-out;
  padding: 15px;
  display: inline-block;
  text-decoration: none !important;
  text-align: center;
  cursor: pointer;

  &:hover {
    background-color: ${constants.cinza1};
  }
`;
