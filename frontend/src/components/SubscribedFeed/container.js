import React, { Component } from "react";
import PropTypes from "prop-types";
import SubscribedFeed from "./presenter";

class Container extends Component {
  state = {
    loading: true,
    height: window.innerHeight
  };
  static propTypes = {
    getSubscribedFeed: PropTypes.func.isRequired,
    subscribedFeed: PropTypes.array
  };
  constructor(props){
    super(props);
    this.handleScroll = this.handleScroll.bind(this);
  } 
  componentDidMount() {
    window.addEventListener("scroll", this.handleScroll);
    const { getSubscribedFeed } = this.props;
    if (!this.props.subscribedFeed || this.props.subscribedFeed.length == 0) {
      // 이미 생성된 feed가 없거나 이전에 생성된 feed 정보가 없는 경우
        getSubscribedFeed(0);
      } else {
        this.setState({
          loading: false
        });
    }
  }
  componentWillUnmount() {
    window.removeEventListener("scroll", this.handleScroll);
  }
  //새로운 prop을 받으면 실행되는 생성주기
  componentWillReceiveProps = nextProps => {
    if (nextProps.subscribedFeed) {
      this.setState({
        loading: false
      });
      if (this.props.subscribedFeed && this.props.subscribedFeed.length== nextProps.subscribedFeed.length){
          window.removeEventListener("scroll", this.handleScroll);
      }
    }
  };

  handleScroll() {
      const { subscribedFeed, getSubscribedFeed } = this.props;
      const windowHeight = "innerHeight" in window ? window.innerHeight : document.documentElement.offsetHeight;
      const body = document.body;
      const html = document.documentElement;
      const docHeight = Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight);
      const windowBottom = windowHeight + window.pageYOffset;
      if (windowBottom >= docHeight && !this.state.loading) {
          this.setState({
            loading: true
          });
          getSubscribedFeed(subscribedFeed[subscribedFeed.length-1].id);
      }
  }
  render() {
    const { subscribedFeed } = this.props;
    return <SubscribedFeed 
            {...this.state} 
            subscribedFeed={subscribedFeed} 
          />;
  }
}

export default Container;