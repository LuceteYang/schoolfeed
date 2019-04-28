import React, { Fragment } from "react";
import PropTypes from "prop-types";
import { Route, Switch } from "react-router-dom";
import styles from "./styles.module.scss";
import Auth from "components/Auth";
import SubscribedFeed from "components/SubscribedFeed";
import SubscribedSchool from "components/SubscribedSchool";
import Search from "components/Search";
import SchoolDetail from "components/SchoolDetail";
import SchoolForm from "components/SchoolForm";
import Navigation from "components/Navigation";
import ProfileContainer from "components/ProfileContainer";


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
    <Route exact path="/" component={SubscribedFeed} />
    <Route path="/feed" component={SubscribedFeed} />
    <Route exact path="/school" component={SubscribedSchool} />
    <Route path="/school/new" component={SchoolForm} />
    <Route exact path="/school/:schoolId" component={SchoolDetail} />
    <Route path="/school/:schoolId/edit" component={SchoolForm} />
    <Route path="/search/:searchTerm" component={Search} />
  	<Route path="/profile" component={ProfileContainer} />
  </Switch>
);

const PublicRoutes = props => (
  <Switch>
      <Route exact path="/" component={Auth} />
  </Switch>
);

export default App;