import React from "react";
import PropTypes from "prop-types";
import formStyles from "shared/formStyles.module.scss";

const LoginForm = (props, context) => (
  <div className={formStyles.formComponent}>
    <form className={formStyles.form} onSubmit={props.handleSubmit}>
      <input
        type="text"
        placeholder="아이디"
        className={formStyles.textInput}
        onChange={props.handleInputChange}
        name="username"
        value={props.usernameValue}
      />
      <input
        type="password"
        placeholder="비밀번호"
        className={formStyles.textInput}
        onChange={props.handleInputChange}
        name="password"
        value={props.passwordValue}
      />
      <input
        type="submit"
        value="로그인"
        className={formStyles.button}
      />
    </form>
    <span className={formStyles.divider}></span>
    <span style={{display: props.errorExist ? 'block':'none'}} className={formStyles.errorMessage}>아이디와 비밀번호를 다시 확인해주세요!</span>
    <span className={formStyles.forgotLink}>
    </span>
  </div>
);
LoginForm.propTypes = {
  handleInputChange: PropTypes.func.isRequired,
  usernameValue: PropTypes.string.isRequired,
  passwordValue: PropTypes.string.isRequired,
  handleSubmit: PropTypes.func.isRequired,
  errorExist: PropTypes.bool.isRequired
};

export default LoginForm;