import React from "react";
import Ionicon from "react-ionicons";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import styles from "./styles.module.scss";

const Navigation = (props, context) => (
  <div className={styles.navigation}>
    <div className={styles.inner}>
      <div className={styles.column}>
        <Link to="/">
        </Link>
      </div>
      <div className={styles.column}>
        <form method="post" onSubmit={props.onSubmit}>
          <input
            type="text"
            placeholder="Search"
            className={styles.searchInput}
            value={props.value}
            onChange={props.onInputChange}
          />
        </form>
      </div>
      <div className={styles.column}>
        <div className={styles.navIcon}>
          <Link to="/explore">
            <Ionicon icon="ios-compass-outline" fontSize="28px" color="black" />
          </Link>
        </div>
        <div className={styles.navIcon}>
          <Link to="/chat">
            <Ionicon icon="ios-chatbubbles-outline" fontSize="28px" color="black" />
          </Link>
        </div>
        <div className={styles.navIcon}>
          <Link to="/profile">
            <Ionicon icon="ios-person-outline" fontSize="32px" color="black" />
          </Link>
        </div>
      </div>
    </div>
  </div>
);
Navigation.propTypes = {
  onInputChange: PropTypes.func.isRequired,
  value: PropTypes.string.isRequired,
  onSubmit: PropTypes.func.isRequired
};


export default Navigation;