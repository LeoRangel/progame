import styled from "styled-components";
import { constants } from "../../styles/constants";

export const Container = styled.div`
  width: 100%;
  text-decoration: none;
  color: black;
  font-size: 0.9em;
  margin-bottom: 10px;
  cursor: pointer;
  padding: 15px;
  display: flex;
  flex-direction: column;
  border: ${constants.borda1};
  border-radius: ${constants.bordaRaioPadrao};
  transition: box-shadow .1s ease-in;
  box-sizing: border-box !important;

  &:hover {
    background-color: rgb(250, 250, 250);
  }
  
  ${(props) => {
    if (props.respondido) {
      return `
        pointer-events: none !important;
      `;
    }
  }}
  
  ${(props) => {
    if (props.selecionada) {
      return `
        box-shadow: 0 0 0 2px ${constants.corPrimaria};
        // background-color: rgb(250, 250, 250);
      `;
    }
    if (props.eliminada) {
      return `
        border: none;
        text-decoration: line-through;
        pointer-events: none;
        cursor: default;

        &:hover {
          background-color: white;
        }
      `;
    }
  }}

  ${(props) => {
    if (props.correta) {
      return `
        box-shadow: 0 0 0 2px ${constants.corNivel1};
      `;
    }
  }}

  ${(props) => {
    if (props.incorreta && props.selecionada) {
      return `
        box-shadow: 0 0 0 2px ${constants.corNivel4};
      `;
    }
  }}

  &.eliminada {
    border: none;
    text-decoration: line-through;
    pointer-events: none;
    cursor: default;

    &:hover {
      background-color: white;
    }
  }
`;
