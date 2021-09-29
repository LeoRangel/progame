export const getNomeNivel = (nivel) => {
  switch (nivel) {
    case 1:
      return "Lembrar";
    case 2:
      return "Entender";
    case 3:
      return "Aplicar";
    case 4:
      return "Analisar";
    case 5:
      return "Avaliar";
    case 6:
      return "Criar";
    default:
      return "";
  }
};

export const getDescricaoNivel = (nivel) => {
  switch (nivel) {
    case 1:
      return "Agora você consegue Lembrar conhecimentos relevantes sobre o assunto estudado!";
    case 2:
      return "...";
    case 3:
      return "...";
    case 4:
      return "...";
    case 5:
      return "...";
    case 6:
      return "...";
    default:
      return "";
  }
};
