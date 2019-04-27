import { connect } from "react-redux";
import { actionCreators as schoolAction } from "redux/modules/school";
import Container from "./container";

const mapStateToProps = (state, ownProps) => {
  const { school: { schoolDetail } } = state;
  return {
    schoolDetail
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