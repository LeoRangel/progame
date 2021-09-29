import styled from "styled-components";
import { constants } from "../../styles/constants";

export const Container = styled.div`
  width: 100%;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
`;

export const Cards = styled.div`
  max-width: 900px;
  padding: 10px;
  display: grid;
  gap: 15px;
  grid-template:
    "pontuacao"
    "rankings"
    "nivel"
    "estudar"
    "footer";

  & > div {
    border-radius: ${constants.bordaRaioPadrao};
    box-shadow: ${constants.sombra1};
    width: 100%;
  }

  @media (max-width: 768px) {
    grid-template:
      "pontuacao"
      "rankings"
      "nivel"
      "estudar"
      "footer";
  }
`;

export const Titulo = styled.span`
  font-size: 1em !important;
  // font-weight: bold !important;
  // color: rgb(0, 0, 0, 0.7);
  margin-bottom: 10px !important;
`;

export const Pontuacao = styled.div`
  grid-area: pontuacao;
  // margin-top: 10vh;
  //padding: 40px 40px 70px 40px;
  padding: 50px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: white;

  & .necessario{
    padding: 5px;
    background-color: orange;
    color: white;
  }

  & .header {
    width: 100%;
    display: flex;
    flex-direction: column;
    text-align: center;

    & .titulos {
      font-size: 1.8rem !important;
      font-weight: bold !important;
    }
    & .subtitulos {
      font-size: 1em !important;
    }
  }

  & .infos {
    margin-top: 50px;
    display: grid;
    gap: 50px;
    grid-template-columns: repeat(3, 1fr);
    padding-bottom: 40px;
  }

  & .infos > div {
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 20px;
    border: ${constants.borda1};
  }

  & .infos .icone {
    margin-bottom: 15px;
    font-size: 2em;
  }

  & .infos .texto {
    display: flex;
    flex-direction: column;
    text-align: center;
    font-size: 14px;
    color: rgba(0, 0, 0, 0.7);
  }

  & .infos .texto .qtd {
    font-size: 1.2rem;
    font-weight: bold;
    color: black;
  }

 
  @media (max-width: 768px) {
    margin-top: 5vh;
    padding: 40px 40px 35px 40px;

    & .infos {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: flex-start;
    }

    & .infos > div {
      flex-direction: row;
      justify-content: flex-start;
    }

    & .infos .icone {
      margin: 0 15px 0 0;
      width: 50px;
      display: flex;
      text-align: right;
    }

    & .infos .texto {
      flex-direction: column;
      text-align: left;
    }
  }

  .resultado-pontuacao .infos {
  }
  .resultado-pontuacao .infos > div {
  }
  .resultado-pontuacao .infos .icone {
  }
  .resultado-pontuacao .infos .texto {
  }
`;

export const Nivel = styled.div`
  grid-area: nivel;
  padding: 35px 25px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  text-align: center;
  color: white !important;
  background-color: ${constants.corNeutra};

  & > div {
    height: 100%;
    margin-top: 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    align-items: center;
    text-align: center;
  }

  & .nivel-oa {
    // width: 180px;
    // height: 180px;
    width: 150px;
    height: 150px;
    padding: 20px;
    border: 5px solid white;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    & h1 {
      // font-size: 2.5em;
      font-size: 3em;
      margin: 0;
      // font-weight: bold;
      letter-spacing: 0.25rem;
    }
    & span {
      font-size: 0.8rem;
      // margin: 0;
      text-transform: uppercase;
    }
  }

  & .descricao {
    font-size: 0.9em;
    font-weight: bold;
    margin-top: 10px;
  }
`;

export const Ranking = styled.div`
  grid-area: rankings;
  margin: 0;
  padding: 0;

  & .ranking {
    border-radius: ${constants.bordaRaioPadrao};
    box-shadow: ${constants.sombra1};
    padding: 35px 25px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    text-align: center;
    align-items: center;
    background-color: white;
  }
  & .ranking > div {
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-top: 10px;
  }

  & .posicao {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;

    & h1 {
      font-weight: bold;
      font-size: 2.5em;
    }
    & span {
      font-size: 14px !important;
      color: rgba(0, 0, 0, 0.7) !important;
      margin: 0;
    }
  }

  @media (min-width: 769px) {
    box-shadow: ${constants.sombra1};

    & .ranking:first-child {
      border-radius: ${constants.bordaRaioPadrao} 0 0 ${constants.bordaRaioPadrao};
      box-shadow: none;
    }
    & .ranking:last-child {
      border-radius: 0 ${constants.bordaRaioPadrao} ${constants.bordaRaioPadrao} 0;
      box-shadow: none;
    }
  }

  @media (max-width: 768px) {
    & .ranking:last-child {
      margin-top: 15px;
    }
  }
`;

export const Estudos = styled.div`
  grid-area: estudar;
  min-width: 200px;
  min-height: 200px;
  padding: 35px 25px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  background-color: white;

  & span {
    font-size: 0.9em;
  }

  & .links-wrapper {
    width: 100%;
    margin-top: 15px;
    max-height: 200px;
    overflow-y: auto;
  }

  & .links-estudo-list {
    padding: 0;
    margin: 0;
  }

  & .links-estudo-list li {
    list-style-type: none;
    width: 100%;
    height: 80px;
    background-color: rgba(0, 0, 0, 0.03);
    border-radius: ${constants.bordaRaioPadrao};

    @media (max-width: 447px) {
      height: 120px;
    }
  }

  & .links-estudo-list li a .info {
    @media (max-width: 447px) {
      font-size: 0.8em !important;
      width: 70% !important;
    }
  }

  & .links-estudo-list li a .imagem {
    @media (max-width: 447px) {
      width: 30% !important;
    }
  }

  & .links-estudo-list li:not(:last-of-type) {
    margin-bottom: 10px;
  }

  & .links-estudo-list li a {
    text-decoration: none;
    color: #000;
    display: flex;
    height: inherit;
  }

  & .links-estudo-list li a .imagem {
    width: 20%;
    background-position: center;
    background-size: cover;
    background-repeat: no-repeat;
    // border-radius: ${constants.bordaRaioPadrao};

  }

  & .links-estudo-list li a .info {
    width: 80%;
    padding: 10px;
    font-size: 0.9em;
  }

  & .links-estudo-list li a .info * {
    overflow-wrap: break-word;
  }

  & .links-estudo-list li:hover a .info {
    background-color: rgba(0, 0, 0, 0.04);
  }

  & .links-estudo-list li a .info p {
    margin-bottom: 5px !important;
  }

  & .links-estudo-list li a .info span {
    color: rgba(0, 0, 0, 0.4);
  }
`;

export const Footer = styled.div`
  padding: 0;
  grid-area: footer;
  width: 100%;
  box-shadow: none !important;
  max-width: none !important;
  
  display: flex;
  justify-content: flex-end;
  align-items: center;
  flex-wrap: wrap-reverse !important;
  
  @media (max-width: 768px) {
    flex-direction: column;
    margin-left: 0 !important;
  }
`;

export const BotaoSecundario = styled.a`
  font-weight: normal !important;
  padding: 10px 17px !important;
  // background: #fff !important;
  // color: rgba(0, 0, 0, 0.75) !important;
  color: #fff !important;
  border-radius: ${constants.botaoBordaRaio} !important;
  border-color: #fff !important;
  padding:  13px 26px !important;
  margin-left: 10px;
  
  display: flex;
  justify-content: center;
  align-items: center;

  &:hover {
    text-decoration: none !important;
  }

  @media (max-width: 768px) {
    width: 100%;
    margin-left: 0 !important;
    margin-top: 10px !important;
  }
`;

export const BotaoPadrao = styled.a`
  color: #fff !important;
  background-color: ${constants.corPrimaria} !important;
  border-color: ${constants.corPrimaria} !important;
  border-radius: ${constants.botaoBordaRaio} !important;
  padding:  13px 26px !important;
  margin-left: 10px;

  display: flex;
  justify-content: center;
  align-items: center;

  &:hover {
    background-color: ${constants.corPrimaria} !important;
    cursor: pointer;
    text-decoration: none !important;
  }

  @media (max-width: 768px) {
    width: 100%;
    margin-left: 0px;
    margin-top: 10px !important;
  }
`;
