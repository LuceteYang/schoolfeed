import React, { Fragment } from "react";
import PropTypes from "prop-types";
import FeedContents from "components/FeedContents";


const Feed = props => (
	<Fragment>
		{props.feed.map(contents => <FeedContents {...contents} key={contents.id} />)}
	</Fragment>
);


Feed.propTypes = {
  	feed: PropTypes.array
};

export default Feed;