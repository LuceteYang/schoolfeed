import React, { Component } from "react";
import PropTypes from "prop-types";
import School from "./presenter";

class Container extends Component {
  state = {
    loading: true
  };
  static propTypes = {
    // searchByTerm: PropTypes.func.isRequired,
    // userList: PropTypes.array,
    // imageList: PropTypes.array
  };

  render() {
    // const { userList, imageList } = this.props;
    return (
      <School {...this.state} />
    );
  }
}

export default Container;