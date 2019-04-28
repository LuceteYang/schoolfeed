import React, { Component } from "react";
import PropTypes from "prop-types";
import SignupForm from "./presenter";

class Container extends Component {
  state = {
    email: "",
    name: "",
    username: "",
    password: "",
    errorMessage:""
  };
  static propTypes = {
    createAccount: PropTypes.func.isRequired,
    errorMessage: PropTypes.string
  };
  // {"username":["This field may not be blank."],"name":["This field may not be blank."]}
  componentWillReceiveProps = nextProps => {
    const { errorMessage } = nextProps;
    if(errorMessage){
      this.setState({
        errorMessage: errorMessage
      });
    }
  };
  render() {
    const { email, name, username, password, errorMessage } = this.state;
    return (
      <SignupForm
        emailValue={email}
        nameValue={name}
        usernameValue={username}
        passwordValue={password}
        handleInputChange={this._handleInputChange}
        handleSubmit={this._handleSubmit}
        errorMessage={errorMessage}
      />
    );
  }
  _handleInputChange = event => {
    const { target: { value, name } } = event;
    this.setState({
      [name]: value
    });
  };
  _handleSubmit = event => {
    const { username, password, email, name } = this.state;
    const { createAccount } = this.props;
    event.preventDefault();
    if(!username){
      return this.setState({
        errorMessage: "아이디를 입력해주세요."
      });
    }
    if(!password){
       this.setState({
        errorMessage: "비밀번호는 8자 이상 12자 이하로 입력해 주세요."
      });
       return
    }
    if(password.length<8){
      this.setState({
        errorMessage: "비밀번호는 8자 이상 12자 이하로 입력해 주세요."
      });
      return
    }
    if(!name){
      return this.setState({
        errorMessage: "이름을 입력해주세요."
      });
    }
    var emailReg = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if(!emailReg.test(email)){
      return this.setState({
        errorMessage: "이메일을 입력해주세요."
      });
    }
    createAccount(username, password, email, name);
  };
}

export default Container;