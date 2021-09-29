import { createGlobalStyle } from "styled-components";
import { constants } from "../styles/constants";

export default createGlobalStyle`
    * {
        margin: 0;
        padding: 0;
        outline: 0;
        box-sizing: border-box;
    }
    
    /* html, body, #root {
        height: 100%;
    } */
    
    body, input, button {
        font-family: ${constants.fontPrimaria};
        font-size: 16px;
    }

    a{
        color: ${constants.corPrimaria};
    }
    a:hover{
        color: ${constants.corPrimariaHover};
    }

    .bgNivel0{
        background-color: ${constants.corNeutra};
        // color: rgb(0, 0, 0, 0.7) !important;
        
        // & .nivel-oa{
        //     border-color: rgb(0, 0, 0, 0.1) !important;
        //     color: rgb(0, 0, 0, 0.1) !important;
        // }
    }
    .bgNivel1{
        background-color: ${constants.corNivel1};
    }
    .bgNivel2{
        background-color: ${constants.corNivel2};
    }
    .bgNivel3{
        background-color: ${constants.corNivel3};
    }
    .bgNivel4{
        background-color: ${constants.corNivel4};
    }
    .bgNivel5{
        background-color: ${constants.corNivel5};
    }
    .bgNivel6{
        background-color: ${constants.corNivel6};
    }

    .text-success{
        color: ${constants.corNivel1} !important;
    }
    .text-danger{
        color: ${constants.corNivel4} !important;
    }
    .text-warning{
        color: ${constants.corNivel6} !important;
    }
    .text-info{
        color: ${constants.corNivel2} !important;
    }

    .swal2-styled.swal2-confirm {
        // border: 0;
        border-radius: ${constants.botaoBordaRaio};
        // background: initial;
        background-color: ${constants.corPrimaria};
        // color: #fff;
        // font-size: 1.0625em;
    }
    .swal2-styled.swal2-cancel {
        // border: 0;
        border-radius: ${constants.botaoBordaRaio};
        // background: initial;
        background-color: #fff;
        border-color: rgb(0,0,0,0.8);
        color: rgb(0,0,0,0.8);
        // font-size: 1.0625em;
    }


`;
