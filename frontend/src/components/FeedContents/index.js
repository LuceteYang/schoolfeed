import { connect } from "react-redux";
import Container from "./container";
import { push } from "react-router-redux";

const mapDispatchToProps = (dispatch, ownProps) => {
  const { school } = ownProps;
  return {
    goToSchoolDetail: () => {
      dispatch(push(`/school/${school.id}`));
    }
  };
};
//컨테이너에 연결
export default connect(null,mapDispatchToProps)(Container);