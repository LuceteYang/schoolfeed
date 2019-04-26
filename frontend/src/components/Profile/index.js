import React from "react";
import PropTypes from "prop-types";
import styles from "./styles.module.scss";
import ProfileForm from "components/ProfileForm";

const Profile = (props, context) => (
  <div className={styles.formComponent}>
    <div className={styles.imageUpload}>
      <label>
        <img
          src={props.profile_image ? props.profile_image : require("images/noPhoto.jpg")} 
          alt={props.username}
          className={styles.image}
        />
      </label>
    </div>
    <div className={styles.textInput}>
        {props.name}
    </div>
    <div className={styles.textInput}>
        {props.email}
    </div>
    <button className={styles.button} onClick={props.showEditView}>내 정보 수정하기</button>
    <button className={styles.button} onClick={props.logout}>로그아웃</button>
   </div>
);


Profile.propTypes = {
  logout: PropTypes.func.isRequired
};


export default Profile;