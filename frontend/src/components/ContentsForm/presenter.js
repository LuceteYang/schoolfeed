import React from "react";
import PropTypes from "prop-types";
import styles from "./styles.module.scss";

const ContentsForm = (props, context) => (
<main className={styles.profile}>
    <div className={styles.column}>
      <div className={`${styles.whiteBox} ${styles.formBox}`}>
        <div className={styles.formComponent}>
          <form className={styles.form} onSubmit={props.handleSubmit}>
          <div className={styles.imageUpload}>
            <label>
              <img
                src={props.main_image ? props.main_image : require("images/noPhoto.jpg")} 
                alt={props.text}
                className={styles.image}
              />
              <input className={styles.fileInput} onChange={props.onChange} id="file-input" type="file" />
            </label>
          </div>
            <input
              type="text"
              placeholder="내용"
              className={styles.textInput}
              value={props.text}
              onChange={props.handleInputChange}
              name="text"
            />
            <input
              type="submit"
              value={props.action==="new"?'등록하기':'수정하기'}
              className={styles.button}
            />
          </form>
          { props.action==="edit" && (<button className={styles.button} onClick={()=>{props.contentsDelete()}}>
            삭제
          </button>)}
          <span style={{display: props.errorMessage ? 'block':'none'}} className={styles.errorMessage}>{props.errorMessage}</span>
        </div>
      </div>
    </div>
  </main>
);

ContentsForm.propTypes = {
  // logout: PropTypes.func.isRequired
};


export default ContentsForm;