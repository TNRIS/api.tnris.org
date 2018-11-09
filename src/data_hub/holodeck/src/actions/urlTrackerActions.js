
import {
  SET_URL
} from '../constants/urlTrackerActionTypes';
import ReactGA from 'react-ga';

export const setUrl = (newUrl, history) => {
  const currentUrl = window.location.pathname;
  history.replace(newUrl);
  ReactGA.pageview(newUrl);
  return (dispatch) => {
    dispatch({
      type: SET_URL,
      payload: {previousUrl: currentUrl}
    })
  }
};
