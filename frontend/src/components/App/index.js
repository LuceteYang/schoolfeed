import { connect } from "react-redux";
import Container from "./container";

const mapStateToProps = (state, ownProps) => {
  const { user, router: { location } } = state;
  //pathname을 전달해야 컨테이너에서 path를 알아서 컴포넌트들이 다시 렌더링하게됨
  return {
    isLoggedIn: user.isLoggedIn,
    pathname: location.pathname
  };
};
//컨테이너에 연결
export default connect(mapStateToProps)(Container);