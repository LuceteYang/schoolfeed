import React from "react";
import PropTypes from "prop-types";
import styles from "./styles.module.scss";
import Loading from "components/Loading";
import SchoolDisplay from "components/SchoolDisplay";

const Search = (props, context) => {
  return (
    <div className={styles.school}>
      <div className={styles.section}>
        <h4 className={styles.title}>검색 결과</h4>
        {props.loading && <Loading />}
        {!props.loading &&
          props.searchSchool.length < 1 && (
            <NotFound text={"해당 학교 페이지가 없습니다."} />
          )}
          <div className={styles.content}>
          {!props.loading && 
              props.searchSchool.length > 0 && (
              <RenderSubscribedSchool schools={props.searchSchool} />
            )}
        </div>
      </div>
    </div>
  );
};

const RenderSubscribedSchool = props =>
  props.schools.map(school => (
    <SchoolDisplay big={false} vertical={true} school={school} key={school.id} />
  ));

const NotFound = props => <span className={styles.notFound}>{props.text}</span>;


Search.propTypes = {
  loading: PropTypes.bool.isRequired,
};

export default Search;