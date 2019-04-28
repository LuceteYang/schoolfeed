import React from "react";
import PropTypes from "prop-types";
import styles from "./styles.module.scss";
import Ionicon from "react-ionicons";

const ContentsForm = (props, context) => (
<main className={styles.profile}>
    <div className={styles.column}>
      <div className={`${styles.whiteBox} ${styles.formBox}`}>
        <div className={styles.formComponent}>
          <form className={styles.form} onSubmit={props.handleSubmit}>
          {props.main_image &&(
            <div className={styles.imageUpload}>
              <label>
                <img
                  src={props.main_image} 
                  alt={props.text}
                  className={styles.image}
                />
                <input className={styles.fileInput} onChange={props.onChange} type="file" />
              </label>
            </div>
            )}
            <textarea
              placeholder="내용"
              className={styles.textInput}
              value={props.text}
              onChange={props.handleInputChange}
              name="text"
            />
            {!props.main_image &&(
              <label>
                <input className={styles.fileInput} onChange={props.onChange}  type="file" />
                <Ionicon className={styles.inputIcon}icon="ios-photos-outline" fontSize="28px" color="black" />
              </label>
            )}
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
  id: PropTypes.number,
  main_image: PropTypes.string,
  text: PropTypes.string,
  loading: PropTypes.bool.isRequired,
  action: PropTypes.string,
  onChange: PropTypes.func.isRequired,
  handleInputChange: PropTypes.func.isRequired,
  handleSubmit: PropTypes.func.isRequired,
  contentsDelete: PropTypes.func.isRequired,
  errorMessage: PropTypes.string
};


export default ContentsForm;