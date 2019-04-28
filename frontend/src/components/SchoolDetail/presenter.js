import React from "react";
import PropTypes from "prop-types";
import styles from "./styles.module.scss";
import Loading from "components/Loading";
import Feed from "components/Feed";


const SchoolDetail = props => {
  if (props.schoolDetail) {
    return <RenderSchoolDetail {...props} />;
  }else if (props.loading) {
    return <LoadingFeed />;
  }
};

const LoadingFeed = props => (
  <div className={styles.feed}>
    <Loading />
  </div>
);

const RenderSchoolDetail = props => (
    <div className={styles.feed}>
      <SchoolInfo {...props}/>
      <Feed feed={props.schoolDetail.contents} />
      {props.loading && <Loading />}
    { props.schoolDetail.contents.length < 1 && (
      <NotFound />
    )}
    </div>
);
const SchoolInfo = props => (
    <div  className={styles.container} >
    	<div className={styles.profile}>
	        <img
	          src={props.schoolDetail.image ? props.schoolDetail.image : require("images/noPhoto.jpg")} 
	          alt={props.schoolDetail.name}
	          className={styles.info.image}
	        />
    	</div>
    	<div className={styles.info}>
    	<h2>
    		{props.schoolDetail.name}
    	</h2>
    	<ul>
    	{props.schoolDetail.location &&(
	    	<li>
	    		지역 : {props.schoolDetail.location}
	    	</li>
    		)}
	    	<li>
	    		구독자수 : {props.schoolDetail.subscriber_count}
	    	</li>
    	</ul>
      <button className={styles.button} onClick={()=>{props.handleClick(props.schoolDetail.is_subscribed)}}>
        {props.schoolDetail.is_subscribed ? "구독취소" : "구독"}
      </button>
      {props.schoolDetail.is_manager && (
      <>
        <button className={styles.button} onClick={()=>{props.goToSchoolEdit()}}>
          수정
        </button>
        <button className={styles.button} onClick={()=>{props.schoolDelete()}}>
          삭제
        </button>
        <button className={styles.button} onClick={()=>{props.handleClick(props.schoolDetail.is_subscribed)}}>
          글 등록
        </button>
      </>
      )}
    	</div>
    </div>
);
const NotFound = props => (
  <div className={styles.notFound}>
    구독중인 학교에 뉴스피드가 없습니다.
    <br/>
    <br/>
    뉴스피드를 받고싶은 학교를 검색해서 구독해주세요!!
  </div>
);

SchoolDetail.propTypes = {
  loading: PropTypes.bool.isRequired,
  handleClick: PropTypes.func.isRequired,
};

export default SchoolDetail;