
import {
  SET_URL
} from '../constants/urlTrackerActionTypes';

export const setUrl = (newUrl, history) => {
  const currentUrl = window.location.pathname;
  console.log(currentUrl);
  console.log(history);
  history.replace(newUrl);
  return (dispatch) => {
    dispatch({
      type: SET_URL,
      payload: {previousUrl: currentUrl}
    })
  }
};
