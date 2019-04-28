import React from "react";
import PropTypes from "prop-types";
import styles from "./styles.module.scss";
import Loading from "components/Loading";
import SchoolDisplay from "components/SchoolDisplay";

const SubscribedSchool = (props, context) => {
  return (
    <div className={styles.school}>
      <div className={styles.section}>
        <h4 className={styles.title}>구독중인 학교</h4>
        <button className={styles.button} onClick={props.goToSchoolNew}>
          학교 생성
        </button>
        {props.loading && <Loading />}
        {!props.loading &&
          props.subscribedSchool.length < 1 && (
            <NotFound text={"구독중인 학교가 없습니다."} />
          )}
          <div className={styles.content}>
          {!props.loading && 
              props.subscribedSchool.length > 0 && (
              <RenderSubscribedSchool schools={props.subscribedSchool} />
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


SubscribedSchool.propTypes = {
  loading: PropTypes.bool.isRequired,
  goToSchoolNew: PropTypes.func.isRequired,
  subscribedSchool: PropTypes.array
};

export default SubscribedSchool;