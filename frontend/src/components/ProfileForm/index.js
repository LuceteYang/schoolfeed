import React from "react";
import PropTypes from "prop-types";
import styles from "./styles.module.scss";

const ProfileForm = (props, context) => (
  <div className={styles.formComponent}>
	  <div className={styles.imageUpload}>
	    <label>
	      <img
	        src={props.profile_image ? props.profile_image : require("images/noPhoto.jpg")} 
	        alt={props.name}
	        className={styles.image}
	      />
	      <input className={styles.fileInput} onChange={props.onChange} id="file-input" type="file" />
	    </label>
	  </div>
    <form className={styles.form} onSubmit={props.handleSubmit}>
      <input
        type="text"
        placeholder="이름"
        className={styles.textInput}
        value={props.name}
        onChange={props.handleInputChange}
        name="name"
      />
      <input
        type="email"
        placeholder="이메일"
        className={styles.textInput}
        value={props.email}
        onChange={props.handleInputChange}
        name="email"
      />
      <input
        type="password"
        placeholder="비밀번호"
        className={styles.textInput}
        value={props.password}
        onChange={props.handleInputChange}
        name="password"
      />
      <input
        type="submit"
        value="수정하기"
        className={styles.button}
      />
    </form>
    <span style={{display: props.errorMessage ? 'block':'none'}} className={styles.errorMessage}>{props.errorMessage}</span>
  </div>
);

ProfileForm.propTypes = {
  profile_image: PropTypes.string.isRequired,
  editShow: PropTypes.bool.isRequired,
  onChange: PropTypes.func.isRequired,
  handleSubmit: PropTypes.func.isRequired,
  name: PropTypes.string.isRequired,
  email: PropTypes.string.isRequired,
  password: PropTypes.string.isRequired,
  errorMessage: PropTypes.string
};

export default ProfileForm;