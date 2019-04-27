import React, { Component } from "react";
import PropTypes from "prop-types";
import Search from "./presenter";

class Container extends Component {
  state = {
    loading: true,
    searchInput:"",
  };
  static propTypes = {
    getSearchSchool: PropTypes.func.isRequired,
    searchSchool: PropTypes.array
  };
  componentDidMount() {
    const { getSearchSchool } = this.props;
    getSearchSchool();
  }
  componentDidUpdate = (prevProps, prevState) => {
    const { getSearchSchool } = this.props;
    if (prevProps.match.params !== this.props.match.params) {
      getSearchSchool();
    }
  };
  componentWillReceiveProps = nextProps => {
    const { getSearchSchool, pathname } = this.props;
    if (nextProps.searchSchool) {
      this.setState({
        loading: false
      });
    }
    // if (nextProps.match = == this.props.match) {
    //   searchByTerm();
    // }
    if (nextProps.pathname !== pathname) {
      getSearchSchool();
    }
  };
  render() {
    const { searchSchool } = this.props;
    return (
      <Search 
        {...this.state}  
        searchSchool={searchSchool}
      />
    );
  }
}

export default Container;