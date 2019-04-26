// 스토어 설정/구성 
// 이 스토어에서 여러 리듀서들을 합처줌
import { createStore, combineReducers, applyMiddleware } from  "redux";
import { routerMiddleware, connectRouter } from "connected-react-router";
import createHistory from "history/createBrowserHistory";
import { composeWithDevTools } from "redux-devtools-extension";
import thunk from "redux-thunk";

import user from  'redux/modules/user';
import school from  'redux/modules/school';
import contents from  'redux/modules/contents';

const env = process.env.NODE_ENV;

const history = createHistory();

const middlewares = [thunk, routerMiddleware(history)];

if (env === "development") {
  const { logger } = require("redux-logger");
  middlewares.push(logger);
}

const reducer = combineReducers({
  user,
  school,
  contents,
  router: connectRouter(history),
});

let store;

if (env === "development") {
  store = initialState =>
    createStore(reducer, composeWithDevTools(applyMiddleware(...middlewares)));
} else {
  store = initialState => createStore(reducer, applyMiddleware(...middlewares));
}

export { history };

export default store();
