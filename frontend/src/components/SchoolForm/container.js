import React, { Component } from "react";
import PropTypes from "prop-types";
import SchoolEditForm from "./presenter";

class Container extends Component {
  state = {
    id:null,
    name:"",
    location:"",
    image:null,
    file:null,
    loading:true,
    action:"new"
  };
  componentDidMount() {
      if(this.props.location.pathname==="/school/new"){
        // 학교 생성
        this.setState({
          action: "new"
        });
      }else if (this.props.location.pathname.match(/^\/school\/(\d+)\/edit/)){
        // 학교 수정
        fetch(`/api/schools/${this.props.match.params.schoolId}/`, {
          headers: {
            Authorization: `JWT ${this.props.token}`,
            "Content-Type": "application/json"
          }
        })
        .then(response => {
          return response.json();
        }).
        then(json =>{
          if (json.is_manager===false){
            return this.props.goToHome()
          }
          this.setState({
            id:json.id,
            name:json.name,
            image:json.image,
            location:json.location,
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
      const { name, location, file, action } = this.state;
      const {match: { params }, token }= this.props
      event.preventDefault();
      if(!name){
        this.setState({
          errorMessage: "학교 이름을 입력해 주세요."
        });
        return
      }
      if(!location){
        return this.setState({
          errorMessage: "지역을 입력해주세요."
        });
      }
      const formData = new FormData()
      formData.append('name',name)
      formData.append('location',location)
      if(file){
        const files = Array.from(file)
        files.forEach((file, i) => {
          formData.append('image', file)
        })
      }
      let url
      let method
      let message
      if(action==="new"){
        url = `/api/schools/`
        method = "POST"
        message = "생성"
      }else if(action==="edit"){
        url = `/api/schools/${params.schoolId}/`
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
      }).
      then(json =>{
        alert(`${message}되었습니다!`)
        this.props.goToSchool(json.id)
      })
    };
  _onChange = (e) =>{
      this.setState({
        image: URL.createObjectURL(e.target.files[0]),
        file: e.target.files
      })
  }


  render() {
    const { schoolDetail, handleClick } = this.props;
    return (
      <SchoolEditForm 
          {...this.state} 
          onChange = {this._onChange} 
          handleInputChange = {this._handleInputChange} 
          handleSubmit = {this._handleSubmit} 
      />
    );
  }
}

export default Container;