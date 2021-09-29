import styled from "styled-components";
import { constants } from "../../styles/constants";

export const Nav = styled.nav`
  height: ${constants.navbarQuestoesHeight};
  font-size: 0.9em;
  font-weight: 600 !important;
  transition: margin-left 0.5s;
  z-index: 8 !important;
  background-color: white;
  color: ${constants.cinza2};
  position: fixed;
  top: 0;
  right: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
`;

export const LogoLink = styled.a`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 140px;
  max-height: 100%;

  &:active img {
    width: 130px !important;
    margin-left: 3px;
  }
`

export const Logo = styled.img`
  //height: 80%;
  width: 140px;

  @media (max-width: 360px) {
    //height: 60%;
  }
`;

export const QuestoesCounter = styled.div`
  display: inline-block;
  color: ${constants.cinza2};
  letter-spacing: 1px;
  font-size: 20px;
  cursor: default;

  @media (min-width: 1496px) {
    display: none;
  }
`;

export const CloseLink = styled.a`
  text-decoration: none;
  color: ${constants.cinza2};
  font-size: 1em;
  display: flex;
  float: left;
  margin-right: 10px;

  &:hover {
    color: ${constants.cinza3};
  }
`;

export const BarraDeProgresso = styled.div`
  z-index: 8 !important;
  position: fixed;
  top: ${constants.navbarQuestoesHeight};
  right: 0;
  left: 0;
`;

export const Progresso = styled.div`
  --progress: ${(props) => props.progresso};
  height: ${constants.progressBarHeight};
  background-color: ${constants.cinza1};
  display: flex;
  flex-flow: row nowrap;
  justify-content: flex-start;

  &::before {
    content: "";
    width: calc(var(--progress) * 1%);
    background-color: ${constants.corPrimaria};
    transition: all 0.2s ease;
  }
`;
