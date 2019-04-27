import React, { Component } from "react";
import PropTypes from "prop-types";
import SchoolDetail from "./presenter";

class Container extends Component {
  state = {
    loading: true,
    height: window.innerHeight
  };
  static propTypes = {
    getSchoolDetail: PropTypes.func.isRequired,
    getSchoolContents: PropTypes.func.isRequired
  };
  constructor(props){
    super(props);
    this.handleScroll = this.handleScroll.bind(this);
  }
  componentDidMount() {
    window.addEventListener("scroll", this.handleScroll);
    console.log(this.props)
    const { getSchoolDetail } = this.props;
	getSchoolDetail();
  }
  componentWillUnmount() {
    window.removeEventListener("scroll", this.handleScroll);
  }
  componentWillReceiveProps = nextProps => {
    if (nextProps.schoolDetail) {
      this.setState({
        loading: false
      });
    if (this.props.schoolDetail && this.props.schoolDetail.contents.length== nextProps.schoolDetail.contents.length){
          window.removeEventListener("scroll", this.handleScroll);
      }
    }
  };
  handleScroll() {

      const { schoolDetail, getSchoolContents } = this.props;
      const windowHeight = "innerHeight" in window ? window.innerHeight : document.documentElement.offsetHeight;
      const body = document.body;
      const html = document.documentElement;
      const docHeight = Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight);
      const windowBottom = windowHeight + window.pageYOffset;
      if (windowBottom >= docHeight && !this.state.loading) {
          this.setState({
            loading: true
          });
          getSchoolContents(schoolDetail.contents[schoolDetail.contents.length-1].id);
      }
  }
  render() {
    const { schoolDetail, handleClick } = this.props;
    return (
      <SchoolDetail 
      {...this.state}
        handleClick={handleClick}
        schoolDetail={schoolDetail}
      />
    );
  }
}

export default Container;