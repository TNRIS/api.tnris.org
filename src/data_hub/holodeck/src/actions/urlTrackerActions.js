
import {
  SET_URL,
  LOG_FILTER_CHANGE,
  CLEAR_PREVIOUS_URL
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

export const logFilterChange = (url) => {
  return (dispatch) => {
    dispatch({
      type: LOG_FILTER_CHANGE,
      payload: {catalogFilterUrl: url}
    })
  }
};

export const clearPreviousUrl = () => {
  return (dispatch) => {
    dispatch({
      type: CLEAR_PREVIOUS_URL
    })
  }
};
