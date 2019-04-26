import React, { Fragment } from "react";
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
      <Feed feed={props.subscribedFeed} />
      {props.loading && <Loading />}
    </div>
);


SubscribedFeed.propTypes = {
  loading: PropTypes.bool.isRequired,
  subscribedFeed: PropTypes.array
};

export default SubscribedFeed;