import React, { Fragment } from "react";
import PropTypes from "prop-types";
import { Route, Switch } from "react-router-dom";
import styles from "./styles.module.scss";
import Auth from "components/Auth";
import Navigation from "components/Navigation";


const App = props => (
  <Fragment>
    {props.isLoggedIn ? <Fragment><Navigation /><PrivateRoutes /></Fragment> : <Fragment><PublicRoutes/></Fragment>}
  </Fragment>
);

App.propTypes = {
  isLoggedIn: PropTypes.bool.isRequired
};


const PrivateRoutes = props => (
  <Switch>
  </Switch>
);

const PublicRoutes = props => (
  <Switch>
      <Route exact path="/" component={Auth} />
  </Switch>
);

export default App;