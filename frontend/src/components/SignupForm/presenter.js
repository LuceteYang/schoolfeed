import React from "react";
import PropTypes from "prop-types";
import formStyles from "shared/formStyles.module.scss";

const SignupForm = (props, context) => (
  <div className={formStyles.formComponent}>
    <h3 className={formStyles.signupHeader}>
      스쿨피드에 가입해서 친구들과 <br/>소식을 공유해보아요.
    </h3>
    <span className={formStyles.divider}></span>
    <form className={formStyles.form} onSubmit={props.handleSubmit}>
      <input
        type="username"
        placeholder="아이디"
        className={formStyles.textInput}
        value={props.usernameValue}
        onChange={props.handleInputChange}
        name="username"
      />
      <input
        type="password"
        placeholder="비밀번호"
        className={formStyles.textInput}
        value={props.passwordValue}
        onChange={props.handleInputChange}
        name="password"
      />
      <input
        type="text"
        placeholder="이름"
        className={formStyles.textInput}
        value={props.nameValue}
        onChange={props.handleInputChange}
        name="name"
      />
      <input
        type="email"
        placeholder="이메일"
        className={formStyles.textInput}
        value={props.emailValue}
        onChange={props.handleInputChange}
        name="email"
      />
      <input
        type="submit"
        value="가입하기"
        className={formStyles.button}
        onChange={props.handleInputChange}
      />
    </form>
    <span style={{display: props.errorMessage ? 'block':'none'}} className={formStyles.errorMessage}>{props.errorMessage}</span>
  </div>
);

SignupForm.propTypes = {
  emailValue: PropTypes.string.isRequired,
  nameValue: PropTypes.string.isRequired,
  usernameValue: PropTypes.string.isRequired,
  passwordValue: PropTypes.string.isRequired,
  handleInputChange: PropTypes.func.isRequired,
  handleSubmit: PropTypes.func.isRequired,
  errorMessage:PropTypes.string.isRequired
};

export default SignupForm;