import React from "react";
import PropTypes from "prop-types";
import styles from "./styles.module.scss";

const SchoolForm = (props, context) => (
<main className={styles.profile}>
    <div className={styles.column}>
      <div className={`${styles.whiteBox} ${styles.formBox}`}>
        <div className={styles.formComponent}>
          <form className={styles.form} onSubmit={props.handleSubmit}>
          <div className={styles.imageUpload}>
            <label>
              <img
                src={props.image ? props.image : require("images/13229625.jpg")} 
                alt={props.name}
                className={styles.image}
              />
              <input className={styles.fileInput} onChange={props.onChange} id="file-input" type="file" />
            </label>
          </div>
            <input
              type="text"
              placeholder="학교 이름"
              className={styles.textInput}
              value={props.name}
              onChange={props.handleInputChange}
              name="name"
            />
            <input
              type="text"
              placeholder="학교 위치"
              className={styles.textInput}
              value={props.location}
              onChange={props.handleInputChange}
              name="location"
            />
            <input
              type="submit"
              value={props.action==="new"?'학교 등록하기':'학교 수정하기'}
              className={styles.button}
            />
          </form>
          <span style={{display: props.errorMessage ? 'block':'none'}} className={styles.errorMessage}>{props.errorMessage}</span>
        </div>
      </div>
    </div>
  </main>
);

SchoolForm.propTypes = {
  id: PropTypes.number,
  name: PropTypes.string.isRequired,
  location: PropTypes.string.isRequired,
  image: PropTypes.string,
  action: PropTypes.string,
  onChange: PropTypes.func.isRequired,
  handleInputChange: PropTypes.func.isRequired,
  handleSubmit: PropTypes.func.isRequired,
  errorMessage: PropTypes.string
};


export default SchoolForm;