import { connect } from "react-redux";
import { actionCreators as userActions } from "redux/modules/user";
import Container from "./container";
import { push } from "react-router-redux";


const mapStateToProps = (state, ownProps) => {
  const { user: { token } } = state;
  return {
    token
  };
};

const mapDispatchToProps = (dispatch, ownProps) => {
	
  return {
    logout: () => {
      dispatch(userActions.logout());
      dispatch(push('/'));
    }
  };
};
export default connect(mapStateToProps, mapDispatchToProps)(Container);