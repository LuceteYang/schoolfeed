import { connect } from "react-redux";
import { actionCreators as contentsActions } from "redux/modules/contents";
import Container from "./container";

const mapStateToProps = (state, ownProps) => {
  const { contents: { subscribedFeed } } = state;
  return {
    subscribedFeed
  };
};


const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    getSubscribedFeed: (last_contents_id) => {
      dispatch(contentsActions.getSubscribedFeed(last_contents_id));
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Container);
