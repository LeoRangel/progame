import React, { Component } from "react";
import { Provider } from "react-redux";
import store from "../store";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import Page404 from "./Page404";
import StartPage from "./StartPage";
import QuizPage from "./QuizPage";
import ResultadoPage from "./ResultadoPage";

import GlobalStyles from "../styles/global";

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <Router>
          <Switch>
            <Route path="/quiz/:modulo/:nivel/" exact component={StartPage} />
            <Route
              path="/quiz/:modulo/:nivel/play/"
              exact
              component={QuizPage}
            />
            <Route
              path="/quiz/:modulo/:nivel/resultado/"
              exact
              component={ResultadoPage}
            />

            {/* If nothing matches... */}
            <Route component={Page404} />
          </Switch>
        </Router>
        <GlobalStyles />
      </Provider>
    );
  }
}

export default App;
