import { connect } from "react-redux";
import Container from "./container";
import { actionCreators as userActions } from "redux/modules/user";

const mapStateToProps = (state, ownProps) => {
  const { user:{authError} } = state;
  let errorMessage = ""
  if(authError){
    var keys = Object.keys(authError)
    errorMessage = authError[keys[0]][0]|| "check fields";
  }
  return {
    errorMessage
  };
};

const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    createAccount: (username, password, email, name) => {
      dispatch(userActions.createAccount(username, password, email, name));
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Container);