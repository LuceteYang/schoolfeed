import React from "react";
import PropTypes from "prop-types";
import styles from "./styles.module.scss";
import { Link } from "react-router-dom";

const SchoolDisplay = (props, context) => (
  <div className={props.horizontal ? styles.horizontal : styles.vertical}>
    <Link to={`/school/${props.school.id}`}>
    <div className={styles.column}>
      <img
        src={props.school.image || require("images/school.png")}
        alt={props.school.name}
        className={props.big ? styles.bigAvatar : styles.avatar}
      />
      <div className={styles.user}>
        <span className={styles.username}>{props.school.name}</span>
        <span className={styles.name}>{props.school.location}</span>
      </div>
    </div>
    </Link>
    <span className={styles.column}>
      <button className={styles.button} onClick={props.handleClick}>
        {props.school.is_subscribed ? "구독취소" : "구독"}
      </button>
    </span>
  </div>
);

SchoolDisplay.propTypes = {
  school: PropTypes.shape({
    id: PropTypes.number.isRequired,
    image: PropTypes.string,
    name: PropTypes.string.isRequired,
    location: PropTypes.string,
    is_subscribed: PropTypes.bool.isRequired
  }).isRequired,
  big: PropTypes.bool,
  handleClick: PropTypes.func.isRequired,
  horizontal: PropTypes.bool,
  vertical: PropTypes.bool
};

export default SchoolDisplay;