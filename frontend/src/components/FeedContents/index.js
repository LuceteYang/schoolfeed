import React, { Fragment } from "react";
import PropTypes from "prop-types";
import styles from "./styles.module.scss";
import TimeStamp from "components/TimeStamp";
import { Link } from "react-router-dom";
import Ionicon from "react-ionicons";

const FeedContents = (props, context) => {
    return (
    <div className={styles.feedContents}>
      <header className={styles.header}>
      <div className={styles.contentsImage}>
    		<img
    			src={props.creator.profile_image || require("images/noPhoto.jpg")}
    			alt={props.creator.name}
    			className={styles.image}
    		/>
        </div>
    		<div className={styles.headerColumn}>
    			<span className={styles.creator}>{props.creator.name}</span>
    			<span className={styles.location}><Link to={`/school/${props.school.id}`}>{props.school.name}</Link>{'\u00A0'}{'\u00A0'}{'\u00A0'}<TimeStamp time={props.natural_time} /></span>
        </div>
        <div className={styles.editIconArea} >
          {props.is_mine && (<Link to={`/school/${props.school.id}/contents/${props.id}`}>
          <Ionicon className={styles.editIcon} icon="ios-create-outline" fontSize="28px" color="black" />
          </Link>)}
        </div>
      </header>

      {props.main_image && <img src={props.main_image} alt={props.text} />}
	  <div className={styles.meta}>
      {props.text.split('\n').map((item, key) => {
        return <Fragment key={key}>{item}<br/></Fragment>
      })}
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
  is_mine: PropTypes.bool.isRequired,
  natural_time: PropTypes.string.isRequired
};

export default FeedContents;