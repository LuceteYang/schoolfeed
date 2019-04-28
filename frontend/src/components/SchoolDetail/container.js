import React, { Component } from "react";
import PropTypes from "prop-types";
import SchoolDetail from "./presenter";
import { confirmAlert } from 'react-confirm-alert'; // Import
import 'react-confirm-alert/src/react-confirm-alert.css'; // Import css
import axios from 'axios';

class Container extends Component {
  state = {
    loading: true,
    height: window.innerHeight
  };
  static propTypes = {
    getSchoolDetail: PropTypes.func.isRequired,
    getSchoolContents: PropTypes.func.isRequired,
    goToSchoolEdit: PropTypes.func.isRequired,
    goToContentsNew: PropTypes.func.isRequired,
    goToSubscribeSchool: PropTypes.func.isRequired,
    handleClick: PropTypes.func.isRequired,
    token: PropTypes.string.isRequired
  };
  constructor(props){
    super(props);
    this.handleScroll = this.handleScroll.bind(this);
  }
  componentDidMount() {
    window.addEventListener("scroll", this.handleScroll);
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
    if (this.props.schoolDetail && this.props.schoolDetail.contents.length === nextProps.schoolDetail.contents.length){
          window.removeEventListener("scroll", this.handleScroll);
      }
    }
  };
  _schoolDelete = () => {
    confirmAlert({
      title: this.props.schoolDetail.name+'학교 페이지를 삭제하시겠습니까?',
      buttons: [
        {
          label: 'Yes',
          onClick: () => {
              let axiosConfig = {
                headers: {
                    Authorization: `JWT ${this.props.token}`
                }
              };
              axios.delete(`/api/schools/${this.props.schoolDetail.id}/`,axiosConfig)
                .then(res => {
                  alert("삭제 되었습니다.")
                  this.props.goToSubscribeSchool()
                })
          }
        },
        {
          label: 'No',
          onClick: () => {}
        }
      ]
    });
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
    const { schoolDetail, handleClick, goToSchoolEdit, goToContentsNew } = this.props;
    return (
      <SchoolDetail 
      {...this.state}
        handleClick={handleClick}
        goToSchoolEdit={goToSchoolEdit}
        schoolDetail={schoolDetail}
        goToContentsNew={goToContentsNew}
        schoolDelete={this._schoolDelete}
      />
    );
  }
}

export default Container;