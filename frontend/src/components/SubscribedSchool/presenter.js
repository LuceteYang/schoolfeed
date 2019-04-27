import React from "react";
import PropTypes from "prop-types";
import styles from "./styles.module.scss";
import Loading from "components/Loading";
// import UserDisplay from "components/UserDisplay";
// import PhotoDisplay from "components/PhotoDisplay";

const Search = (props, context) => {
  return (
    <div className={styles.search}>
      <div className={styles.section}>
        <h4 className={styles.title}>{"Users"}</h4>
        {props.loading && <Loading />}
        {!props.loading &&
          props.userList.length < 1 && (
            <NotFound text={"Nothing found :("} />
          )}
        <div className={styles.content}>
          {!props.loading && (
              <RenderUserSearch userList={props.userList} />
            )}
        </div>
      </div>
    </div>
  );
};

const RenderUserSearch = props => (
    <div>
      RenderUserSearch
    </div>
  )


const NotFound = props => <span className={styles.notFound}>{props.text}</span>;


Search.propTypes = {
  loading: PropTypes.bool.isRequired,
};

export default Search;