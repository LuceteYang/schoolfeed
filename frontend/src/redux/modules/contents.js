// imports
import { actionCreators as userActions } from "redux/modules/user";

// actions

const SET_SUBSCRIBED_FEED = "SET_SUBSCRIBED_FEED";

// action crators

function setSubscribedFeed(last_contents_id,newSubscribedFeed) {
  return {
    type: SET_SUBSCRIBED_FEED,
    newSubscribedFeed,
    last_contents_id
  };
}



function getSubscribedFeed(last_contents_id) {
  return (dispatch, getState) => {
    const { user: { token } } = getState();
    fetch(`/contents/?last_contents_id=${last_contents_id}`, {
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
      .then(json => dispatch(setSubscribedFeed(last_contents_id,json)));
  };
}

// action creators


// initial state
const initialState = {
}

// reducer

function reducer(state = initialState, action){
	switch (action.type){
  	case SET_SUBSCRIBED_FEED:
  		return applySetSubscribedFeed(state, action);
		default:
			return state;
	}
}

// reducer functions
function applySetSubscribedFeed(state, action) {
  const { newSubscribedFeed, last_contents_id } = action;
  const { subscribedFeed } = state;
  let updatedUserList;
  if(last_contents_id == 0 ){
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
  getSubscribedFeed,
};

export { actionCreators };

// reducer export

export default reducer;