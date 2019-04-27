import { connect } from "react-redux";
import Container from "./container";
import { actionCreators as schoolAction } from "redux/modules/school";
import { push } from "react-router-redux";

const mapDispatchToProps = (dispatch, ownProps) => {
  const { school } = ownProps;
  return {
    handleClick: () => {
      if (school.is_subscribed) {
        dispatch(schoolAction.unsubscribeSchool(school.id));
      } else {
        dispatch(schoolAction.subscribeSchool(school.id));
      }
    },
    goToSchoolDetail: () => {
      dispatch(push(`/school/${school.id}`));
    }
  };
};

export default connect(null, mapDispatchToProps)(Container);