import React, { Component } from "react";
import ProfileContainer from "./presenter";
import axios from 'axios';
import PropTypes from "prop-types";

class Container extends Component {
	state = {
    	"email": "",
    	"profile_image":"",
    	"name":"",
	    "password":"",
	    "editShow":false
	};
  static propTypes = {
    logout: PropTypes.func.isRequired,
    token: PropTypes.string.isRequired
  };
	componentDidMount() {
      let axiosConfig = {
        headers: {
            Authorization: `JWT ${this.props.token}`
        }
      };
      axios.get(`/api/users/`,axiosConfig)
        .then(res => {
		    this.setState({
		    	...res.data
		    });
        })
	}
  	_handleInputChange = event => {
	    const { target: { value, name } } = event;
	    this.setState(
	    {
	      	[name]: value
	    });
	  };
  	_handleSubmit = event => {
	    const { password, email, name } = this.state;
	    event.preventDefault();
	    if(password && password.length<8){
	      this.setState({
	        errorMessage: "비밀번호는 8자 이상 12자 이하로 입력해 주세요."
	      });
	      return
	    }
	    if(!name){
	      return this.setState({
	        errorMessage: "이름을 입력해주세요."
	      });
	    }
	    var emailReg = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	    if(!emailReg.test(email)){
	      return this.setState({
	        errorMessage: "이메일을 입력해주세요."
	      });
	    }
	    const formData = new FormData()
	    formData.append('email',email)
	    formData.append('name',name)
	    this._requestChangeProfile(formData)
	    if(password){
	    	this._requestChangePassword()
	    }
	  };
	_onChange = (e) =>{
	    const files = Array.from(e.target.files)
	    const formData = new FormData()

	    files.forEach((file, i) => {
	      formData.append('profile_image', file)
	    })
	    this._requestChangeProfile(formData)
	}
	_requestChangeProfile = formData =>{
	    fetch(`/api/users/`, {
	      method: 'PUT',
	      body: formData,
      	  headers: {
	        Authorization: `JWT ${this.props.token}`
	      }
	    })
	    .then(res => res.json())
	    .then(info => {
	      this.setState({ 
	      	...info,
	      	editShow:false
	      })
	    })
	}
	_requestChangePassword = () =>{
  		axios.post('/rest-auth/password/change/',
		{
			new_password1: this.state.password,
			new_password2: this.state.password
		},
      	{
	        headers: { Authorization: `JWT ${this.props.token}` }
      	})
	    .then(info => {
	      this.setState({ 
	      	"password":""
	      })
	    })
	}
	_showEditView = () =>{
      this.setState({ 
      	"editShow":true
      })
	}
	render() {
    	return <ProfileContainer 
    				{...this.state} 
    				{...this.props} 
    				onChange = {this._onChange} 
    				handleInputChange = {this._handleInputChange} 
    				handleSubmit = {this._handleSubmit} 
    				showEditView = {this._showEditView} 
    			/>;
	}
}

export default Container;