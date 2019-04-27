import React, { Component } from "react";
import PropTypes from "prop-types";
import SubscribedSchool from "./presenter";

class Container extends Component {
  state = {
    loading: true
  };
  static propTypes = {
    getSubscribedSchool: PropTypes.func.isRequired,
    subscribedSchool: PropTypes.array
  };
  componentDidMount() {
    const { getSubscribedSchool } = this.props;
    getSubscribedSchool(1);
  }
  //새로운 prop을 받으면 실행되는 생성주기
  componentWillReceiveProps = nextProps => {
    if (nextProps.subscribedSchool) {
      this.setState({
        loading: false
      });
    }
  };
  render() {
    const { subscribedSchool } = this.props;
    return (
      <SubscribedSchool 
        {...this.state} 
        subscribedSchool={subscribedSchool} 
      />
    );
  }
}

export default Container;