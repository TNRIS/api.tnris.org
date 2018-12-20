
import {
  SET_URL
} from '../constants/urlTrackerActionTypes';
import ReactGA from 'react-ga';

export const setUrl = (newUrl, history) => {
  const currentUrl = window.location.pathname;
  console.log(history);
  console.log(newUrl);
  history.replace(newUrl);
  ReactGA.pageview(newUrl);
  return (dispatch) => {
    dispatch({
      type: SET_URL,
      payload: {previousUrl: currentUrl}
    })
  }
};
