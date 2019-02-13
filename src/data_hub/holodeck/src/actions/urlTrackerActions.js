
import {
  SET_URL,
  LOG_FILTER_CHANGE,
  CLEAR_PREVIOUS_URL
} from '../constants/urlTrackerActionTypes';
import ReactGA from 'react-ga';
import { push, replace } from 'connected-react-router';
import { store } from '../App';

export const setUrl = (newUrl) => {
  const currentUrl = window.location.pathname;
  ReactGA.pageview(newUrl);
  return (dispatch) => {
    const curState = store.getState();
    dispatch(push(newUrl, curState));
    dispatch({
      type: SET_URL,
      payload: {previousUrl: currentUrl}
    });
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

export const url404 = () => {
  const curState = store.getState();
  return (dispatch) => {
    dispatch(replace('/404', curState));
  }
}
