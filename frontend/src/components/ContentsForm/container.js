import React, { Component } from "react";
import PropTypes from "prop-types";
import ContentsForm from "./presenter";
import { confirmAlert } from 'react-confirm-alert'; // Import
import 'react-confirm-alert/src/react-confirm-alert.css'; // Import css
import axios from 'axios';

class Container extends Component {
  state = {
    id:null,
    text:"",
    main_image:null,
    file:null,
    loading:true,
    action:"new"
  };
  static propTypes = {
    goToSchool: PropTypes.func.isRequired,
    goToHome: PropTypes.func.isRequired,
  };
  componentDidMount() {
      if(this.props.location.pathname.match(/^\/school\/(\d+)\/contents/)){
        // 컨텐츠 생성
        this.setState({
          action: "new"
        });
      }else if (this.props.location.pathname.match(/^\/contents\/(\d+)/)){
        // 컨텐츠 수정
        fetch(`/api/contents/${this.props.match.params.contentsId}/`, {
          headers: {
            Authorization: `JWT ${this.props.token}`,
            "Content-Type": "application/json"
          }
        }).then(response => {
          return response.json();
        }).then(json =>{
          if (json.is_mine===false){
            return this.props.goToHome()
          }
          this.setState({
            id:json.id,
            text:json.text,
            school:json.school,
            main_image:json.main_image,
            action:"edit"
          });
        })
      }else{
        // 예외 경우
        return this.props.goToHome()
      }
  }
    _handleInputChange = event => {
      const { target: { value, name } } = event;
      this.setState(
      {
          [name]: value
      });
    };
    _handleSubmit = event => {
      const { text, file, action } = this.state;
      const {match: { params }, token }= this.props
      event.preventDefault();
      if(!text){
        this.setState({
          errorMessage: "내용을 입력해 주세요."
        });
        return
      }
      const formData = new FormData()
      formData.append('text',text)
      if(file){
        const files = Array.from(file)
        files.forEach((file, i) => {
          formData.append('main_image', file)
        })
      }
      let url
      let method
      let message
      if(action==="new"){
        url = `/api/contents/`
        method = "POST"
        message = "생성"
        formData.append('school',params.schoolId)
      }else if(action==="edit"){
        url = `/api/contents/${params.contentsId}/`
        method = "PUT"
        message = "수정"
      }
      fetch(url, {
        method: method,
        body: formData,
          headers: {
          Authorization: `JWT ${token}`
        }
      })
      .then(response => {
        return response.json();
      }).then(json =>{
        alert(`${message}되었습니다!`)
        this.props.goToSchool(json.school)
      })
    };
  _onChange = (e) =>{
      this.setState({
        main_image: URL.createObjectURL(e.target.files[0]),
        file: e.target.files
      })
  }
  _contentsDelete = () => {
    const {match: { params:{contentsId} }, token }= this.props
    confirmAlert({
      title: '이 글을 삭제하시겠습니까?',
      buttons: [
        {
          label: 'Yes',
          onClick: () => {
              let axiosConfig = {
                headers: {
                    Authorization: `JWT ${token}`
                }
              };
              axios.delete(`/api/contents/${contentsId}/`,axiosConfig)
                .then(res => {
                  alert("삭제 되었습니다.")
                  this.props.goToSchool(this.state.school)
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

  render() {
    return (
      <ContentsForm 
          {...this.state} 
          onChange = {this._onChange} 
          handleInputChange = {this._handleInputChange} 
          handleSubmit = {this._handleSubmit} 
          contentsDelete={this._contentsDelete}
      />
    );
  }
}

export default Container;