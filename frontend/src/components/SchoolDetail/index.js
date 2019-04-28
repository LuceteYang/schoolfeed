import { connect } from "react-redux";
import { actionCreators as schoolAction } from "redux/modules/school";
import Container from "./container";
import { push } from "react-router-redux";

const mapStateToProps = (state, ownProps) => {
  const { school: { schoolDetail }, user: { token } } = state;
  return {
    schoolDetail,
    token
  };
};

const mapDispatchToProps = (dispatch, ownProps) => {
  const { match: { params: { schoolId } } } = ownProps;
  return {
    getSchoolDetail: () => {
      dispatch(schoolAction.getSchoolDetail(schoolId));
    },
    getSchoolContents: (lastContentsId) => {
      dispatch(schoolAction.getSchoolContents(schoolId, lastContentsId));
    },
    goToSchoolEdit: () => {
      dispatch(push(`/school/${schoolId}/edit`));
    },
    goToSubscribeSchool: () => {
      dispatch(push(`/school`));
    },
    handleClick: (is_subscribed) => {
      if (is_subscribed) {
        dispatch(schoolAction.unsubscribeSchool(schoolId));
      } else {
        dispatch(schoolAction.subscribeSchool(schoolId));
      }
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Container);