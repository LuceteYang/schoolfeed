// reducer

// imports

// actions
const SAVE_TOKEN = "SAVE_TOKEN";
const LOGOUT = "LOGOUT";
const SET_AUTH_ERROR = "SET_AUTH_ERROR";
const SET_SUBSCRIBED_FEED = "SET_SUBSCRIBED_FEED";


// action crators

function saveAuthError(preload) {
  return {
    type: SET_AUTH_ERROR,
    preload
  };
}

function saveToken(token) {
  return {
    type: SAVE_TOKEN,
    token
  };
}

function logout() {
  return {
    type: LOGOUT
  };
}


function setSubscribedFeed(last_contents_id,newSubscribedFeed) {
  return {
    type: SET_SUBSCRIBED_FEED,
    newSubscribedFeed,
    last_contents_id
  };
}




function usernameLogin(username, password) {
	//dispatch, fetch react-thunk임
  return dispatch => {
    fetch("/api/rest-auth/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username,
        password
      })
    })
      .then(response => response.json())
      .then(json => {
        if (json.token) {
          dispatch(saveToken(json.token));
        }else{
          dispatch(saveAuthError(json));
        }
      })
      .catch(err => {
      });
  };
}
function createAccount(username, password, email, name) {
  return dispatch => {
    fetch("/api/rest-auth/registration/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username,
        password1: password,
        password2: password,
        email,
        name
      })
    })
      .then(response => response.json())
      .then(json => {
        if (json.token) {
          dispatch(saveToken(json.token));
        }else{
          dispatch(saveAuthError(json));
        }
      })
  }
}
function getSubscribedFeed(last_contents_id) {
  return (dispatch, getState) => {
    const { user: { token } } = getState();
    fetch(`/api/users/contents/?last_contents_id=${last_contents_id}`, {
      headers: {
        Authorization: `JWT ${token}`,
        "Content-Type": "application/json"
      }
    })
      .then(response => {
        if (response.status === 401) {
          dispatch(logout());
        }
        return response.json();
      })
      .then(json => dispatch(setSubscribedFeed(last_contents_id,json)));
  };
}



// action creators


// initial state
const initialState = {
	  isLoggedIn: localStorage.getItem("jwt") ? true : false,
    token: localStorage.getItem("jwt")
}

// reducer

function reducer(state = initialState, action){
	switch (action.type){
  	case SAVE_TOKEN:
  		return applySetToken(state, action);
    case LOGOUT:
      return applyLogout(state, action);
    case SET_AUTH_ERROR:
      return applySetAuthError(state, action);
    case SET_SUBSCRIBED_FEED:
      return applySetSubscribedFeed(state, action);
		default:
			return state;
	}
}

// reducer functions
function applySetToken(state, action) {
  const { token } = action;
  localStorage.setItem("jwt", token);
  return {
    ...state,
    isLoggedIn: true,
    token: token
  };
}
function applyLogout(state, action) {
  localStorage.removeItem("jwt");
  // 유저 관련 정보 삭
  delete state['subscribedFeed']
  return {
    ...state,
    isLoggedIn: false
  };
}

function applySetAuthError(state, action){
  const { preload } = action;
  return {
    ...state,
    authError:preload
  }
}

function applySetSubscribedFeed(state, action) {
  const { newSubscribedFeed, last_contents_id } = action;
  const { subscribedFeed } = state;
  let updatedUserList;
  if(last_contents_id === 0 ){
    updatedUserList = newSubscribedFeed;
  }else{
    updatedUserList = subscribedFeed.concat(newSubscribedFeed)
  }
  return {
    ...state,
    subscribedFeed: updatedUserList
  };
}


// exports
const actionCreators = {
  usernameLogin,
  createAccount,
  logout,
  getSubscribedFeed
};

export { actionCreators };

// reducer export

export default reducer;