import React from "react";
import { useParams } from "react-router-dom";
import logo from "../../assets/img/logo.png";
import { FaTimes } from "react-icons/fa";

// Styles
import {
  Nav,
  LogoLink,
  Logo,
  QuestoesCounter,
  CloseLink,
  BarraDeProgresso,
  Progresso,
} from "./styles";

export default function Navbar(props) {
  const { modulo, nivel } = useParams();

  return (
    <>
      <Nav className="navbar navbar-expand-lg">
        <LogoLink href='/aluno/dashboard/'>
          <Logo src={logo} />
        </LogoLink>

        {props.progresso && (
          <QuestoesCounter title="Progresso">
            {props.questaoAtualIndice + 1}/{props.qtdQuestoes}
          </QuestoesCounter>
        )}
        <CloseLink
          title="Sair"
          href={`/aluno/modulo/${modulo}/`}
          className="botao-sair"
        >
          <span>
            <FaTimes size={20} />
          </span>
        </CloseLink>
      </Nav>
      <BarraDeProgresso>
        <Progresso progresso={props.progresso} className="progress-bar" />
      </BarraDeProgresso>
    </>
  );
}
