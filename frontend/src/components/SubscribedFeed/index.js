import { connect } from "react-redux";
import { actionCreators as userActions } from "redux/modules/user";
import Container from "./container";

const mapStateToProps = (state, ownProps) => {
  const { user: { subscribedFeed } } = state;
  return {
    subscribedFeed
  };
};


const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    getSubscribedFeed: (last_contents_id) => {
      dispatch(userActions.getSubscribedFeed(last_contents_id));
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Container);
