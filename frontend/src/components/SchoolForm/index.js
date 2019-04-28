import { connect } from "react-redux";
import { actionCreators as schoolAction } from "redux/modules/school";
import Container from "./container";
import { push } from "react-router-redux";

const mapStateToProps = (state, ownProps) => {
  const { user:{ token } } = state;
  return {
    token
  };
};


const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    goToSchool: (schoolId) => {
      dispatch(push(`/school/${schoolId}`));
    },
    goToHome: () => {
      dispatch(push('/'));
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Container);