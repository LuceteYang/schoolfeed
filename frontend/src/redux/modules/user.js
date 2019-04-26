// reducer

// imports

// actions
const SAVE_TOKEN = "SAVE_TOKEN";
const LOGOUT = "LOGOUT";
const SET_EXPLORE = "SET_EXPLORE";
const SET_IMAGE_LIST = "SET_IMAGE_LIST";
const SET_AUTH_ERROR = "SET_AUTH_ERROR";

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


function setImageList(imageList) {
  return {
    type: SET_IMAGE_LIST,
    imageList
  };
}




function usernameLogin(username, password) {
	//dispatch, fetch react-thunk임
  return dispatch => {
    fetch("/rest-auth/login/", {
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
        console.log(err)
      });
  };
}
function createAccount(username, password, email, name) {
  return dispatch => {
    fetch("/rest-auth/registration/", {
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


// exports
const actionCreators = {
  usernameLogin,
  createAccount,
  logout
};

export { actionCreators };

// reducer export

export default reducer;