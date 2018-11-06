
import {
  SET_URL
} from '../constants/urlTrackerActionTypes';

export const setUrl = (newUrl, history) => {
  const currentUrl = window.location.pathname;
  history.replace(newUrl);
  return (dispatch) => {
    dispatch({
      type: SET_URL,
      payload: {previousUrl: currentUrl}
    })
  }
};
