import { connect } from "react-redux";
import { actionCreators as schoolActions } from "redux/modules/school";
import Container from "./container";

const mapStateToProps = (state, ownProps) => {
  const { school: { subscribedSchool } } = state;
  return {
    subscribedSchool
  };
};

const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    getSubscribedSchool: (page) => {
      dispatch(schoolActions.getSubscribedSchool(page));
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Container);