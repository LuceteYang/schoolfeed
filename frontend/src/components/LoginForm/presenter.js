import React from "react";
import PropTypes from "prop-types";
import Ionicon from "react-ionicons";
import formStyles from "shared/formStyles.module.scss";

const LoginForm = (props, context) => (
  <div className={formStyles.formComponent}>
    <h3 className={formStyles.signupHeader}>
      스쿨피드에 가입해서 친구들과 <br/>소식을 공유해보아요.
    </h3>
    <span className={formStyles.divider}></span>
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
      비밀번호를 잃어버리셨나요?
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

LoginForm.contextTypes = {
  t: PropTypes.func.isRequired
};

export default LoginForm;