import React from "react";
import PropTypes from "prop-types";
import styles from "./styles.module.scss";
import TimeStamp from "components/TimeStamp";

const FeedContents = (props, context) => {
	console.log(props)
    return (
    <div className={styles.feedContents}>
      <header className={styles.header}>
		<img
			src={props.creator.profile_image || require("images/noPhoto.jpg")}
			alt={props.creator.name}
			className={styles.image}
		/>
		<div className={styles.headerColumn}>
			<span className={styles.creator}>{props.creator.name}</span>
			<span className={styles.location}>{props.school.name}{'\u00A0'}{'\u00A0'}{'\u00A0'}<TimeStamp time={props.natural_time} /></span>
        </div>
      </header>

      {props.main_image && <img src={props.main_image} alt={props.text} />}
	  <div className={styles.meta}>
      
      {props.text}
      </div>
    </div>
  );
};

FeedContents.propTypes = {
  id: PropTypes.number.isRequired,
  creator: PropTypes.shape({
    profile_image: PropTypes.string,
    name: PropTypes.string.isRequired
  }).isRequired,
  school: PropTypes.shape({
  	id: PropTypes.number.isRequired,
    location: PropTypes.string,
    name: PropTypes.string.isRequired
  }).isRequired,
  main_image: PropTypes.string,
  text: PropTypes.string.isRequired,
  natural_time: PropTypes.string.isRequired
};

export default FeedContents;