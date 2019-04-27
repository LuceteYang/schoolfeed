import React from "react";
import PropTypes from "prop-types";
import styles from "./styles.module.scss";
import ProfileForm from "components/ProfileForm";
import Profile from "components/Profile";

const ProfileContainer = (props, context) => (
<main className={styles.profile}>
    <div className={styles.column}>
      <div className={`${styles.whiteBox} ${styles.formBox}`}>
        {props.editShow === false && <Profile {...props} />}
        {props.editShow === true && <ProfileForm {...props} />}
      </div>
    </div>
  </main>
);

ProfileContainer.propTypes = {
  logout: PropTypes.func.isRequired
};


export default ProfileContainer;