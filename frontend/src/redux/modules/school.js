// imports
import { actionCreators as userActions } from "redux/modules/user";

// actions

const SET_SUBSCRIBED_SCHOOL = "SET_SUBSCRIBED_SCHOOL";
const SUBSCRIBE_SCHOOL = "SUBSCRIBE_SCHOOL";
const UNSUBSCRIBE_SCHOOL = "UNSUBSCRIBE_SCHOOL";
const SEARCH_SCHOOL = "SEARCH_SCHOOL";

// action crators
function setSubscribedSchool(page,newSubscribedSchool) {
  return {
    type: SET_SUBSCRIBED_SCHOOL,
    newSubscribedSchool,
    page
  };
}

function doSubscribeSchool(schoolId) {
  return {
    type: SUBSCRIBE_SCHOOL,
    schoolId
  };
}

function doUnsubscribeSchool(schoolId) {
  return {
    type: UNSUBSCRIBE_SCHOOL,
    schoolId
  };
}
function setSearchSchool(newSubscribedSchool) {
  return {
    type: SEARCH_SCHOOL,
    newSubscribedSchool,
  };
}


function getSubscribedSchool(page) {
  return (dispatch, getState) => {
    const { user: { token } } = getState();
    fetch(`/schools/?page=${page}`, {
      headers: {
        Authorization: `JWT ${token}`,
        "Content-Type": "application/json"
      }
    })
      .then(response => {
        if (response.status === 401) {
          dispatch(userActions.logout());
        }
        return response.json();
      })
      .then(json => dispatch(setSubscribedSchool(page,json)));
  };
}

function subscribeSchool(schoolId) {
  return (dispatch, getState) => {
    dispatch(doSubscribeSchool(schoolId));
    const { user: { token } } = getState();
    fetch(`/schools/${schoolId}/subscribes/`, {
      method: "POST",
      headers: {
        Authorization: `JWT ${token}`
      }
    }).then(response => {
      if (response.status === 401) {
        dispatch(userActions.logout());
      } else if (!response.ok) {
        dispatch(doUnsubscribeSchool(schoolId));
      }
    });
  };
}

function unsubscribeSchool(schoolId) {
  return (dispatch, getState) => {
    dispatch(doUnsubscribeSchool(schoolId));
    const { user: { token } } = getState();
    fetch(`/schools/${schoolId}/unsubscribes/`, {
      method: "DELETE",
      headers: {
        Authorization: `JWT ${token}`
      }
    }).then(response => {
      if (response.status === 401) {
        dispatch(userActions.logout());
      } else if (!response.ok) {
        dispatch(doSubscribeSchool(schoolId));
      }
    });
  };
}
function getSearchSchool(schoolName) {
  return (dispatch, getState) => {
    const { user: { token } } = getState();
    fetch(`/schools/search/?school_name=${schoolName}`, {
      headers: {
        Authorization: `JWT ${token}`,
        "Content-Type": "application/json"
      }
    })
  .then(response => {
    if (response.status === 401) {
      dispatch(userActions.logout());
    }
    return response.json();
  })
  .then(json => dispatch(setSearchSchool(json)));
  };
}

// action creators


// initial state
const initialState = {
}

// reducer

function reducer(state = initialState, action){
	switch (action.type){
	    case SUBSCRIBE_SCHOOL:
	      return applySubscribeSchool(state, action);
	    case UNSUBSCRIBE_SCHOOL:
	      return applyUnsubscribeSchool(state, action);
	    case SET_SUBSCRIBED_SCHOOL:
	      return applySetSubscribedSchool(state, action);
	    case SEARCH_SCHOOL:
	      return applySearchSchool(state, action);
		default:
			return state;
	}
}

// reducer functions
function applySetSubscribedSchool(state, action) {
  const { newSubscribedSchool, page } = action;
  const { subscribedSchool } = state;
  let updatedSubscribedSchool;
  if(page == 1 ){
    updatedSubscribedSchool = newSubscribedSchool;
  }else{
    updatedSubscribedSchool = subscribedSchool.concat(newSubscribedSchool)
  }
  return {
    ...state,
    subscribedSchool: updatedSubscribedSchool
  };
}

function applySubscribeSchool(state, action) {
  const { schoolId } = action;
  const { subscribedSchool, searchSchool } = state;
  let result = {}
  if (searchSchool){
    const updatedSearchSchools = searchSchool.map(school => {
      if (school.id === schoolId) {
        return { ...school, is_subscribed: true };
      }
      return school;
    });
    result.searchSchool = updatedSearchSchools;
  }
  return { ...state, ...result };
}

function applyUnsubscribeSchool(state, action) {
  const { schoolId } = action;
  const { subscribedSchool, searchSchool } = state;
  let result = {}
  if (subscribedSchool){
    const updatedSubscribedSchools = subscribedSchool.filter(school => school.id!=schoolId);
    result.subscribedSchool = updatedSubscribedSchools;
  }
  if (searchSchool){
    const updatedSearchSchools = searchSchool.map(school => {
      if (school.id === schoolId) {
        return { ...school, is_subscribed: false };
      }
      return school;
    });
    result.searchSchool = updatedSearchSchools;
  }
  return { ...state, ...result };
}
function applySearchSchool(state, action){
  const { newSubscribedSchool } = action;
  return { ...state, searchSchool: newSubscribedSchool };
}

// exports
const actionCreators = {
  	subscribeSchool,
  	unsubscribeSchool,
  	getSubscribedSchool,
  	getSearchSchool,
};

export { actionCreators };

// reducer export

export default reducer;