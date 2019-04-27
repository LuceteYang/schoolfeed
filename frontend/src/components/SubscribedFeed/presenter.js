import React from "react";
import PropTypes from "prop-types";
import styles from "./styles.module.scss";
import Loading from "components/Loading";
import Feed from "components/Feed";


const SubscribedFeed = props => {
  if (props.subscribedFeed) {
    return <RenderFeed {...props} />;
  }else if (props.loading) {
    return <LoadingFeed />;
  }
};

const LoadingFeed = props => (
  <div className={styles.feed}>
    <Loading />
  </div>
);

const RenderFeed = props => (
    <div className={styles.feed}>
    { props.subscribedFeed.length < 1 && (
      <NotFound />
    )}
      <Feed feed={props.subscribedFeed} />
      {props.loading && <Loading />}
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

SubscribedFeed.propTypes = {
  loading: PropTypes.bool.isRequired,
  subscribedFeed: PropTypes.array
};

export default SubscribedFeed;