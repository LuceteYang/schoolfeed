import React from "react";
import styles from "./styles.module.scss";
import LoginForm from "components/LoginForm";
import SignupForm from "components/SignupForm";


const Auth = (props, context) => (
  <main className={styles.auth}>
    <div className={styles.column}>
      <img
        src={require("images/nicole-honeywill-1465559-unsplash-min.jpg")}
        alt="Welcome To SchoolFeed"
        style = {{width:"500px",padding:"1px",border: "1px solid #e6e6e6"}}
      />
    </div>
    <div className={styles.column}>
      <div className={`${styles.whiteBox} ${styles.formBox}`}>
      <img src={require("images/logo.png")} alt="Logo" />
        {props.action === "login" && <LoginForm />}
        {props.action === "signup" && <SignupForm />}
      </div>
	  <div className={styles.whiteBox}>
        {props.action === "signup" && (
          <p>
            아이디가 있으신가?{" "}
            <span className={styles.changeLink} onClick={props.changeAction}>
              로그인
            </span>
          </p>
        )}
        {props.action === "login" && (
          <p>
            아이디가 없으신가요?{" "}
            <span className={styles.changeLink} onClick={props.changeAction}>
              가입하기
            </span>
          </p>
        )}
      </div>
    </div>
  </main>
);
export default Auth;