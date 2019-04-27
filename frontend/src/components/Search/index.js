import { connect } from "react-redux";
import { actionCreators as schoolActions } from "redux/modules/school";
import Container from "./container";

const mapStateToProps = (state, ownProps) => {
  const { school: { searchSchool } } = state;
  return {
    searchSchool,
  };
};

const mapDispatchToProps = (dispatch, ownProps) => {
const { match: { params: { searchTerm } } } = ownProps;
  return {
    getSearchSchool: () => {
      dispatch(schoolActions.getSearchSchool(searchTerm));
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Container);