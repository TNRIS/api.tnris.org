
import {
  SET_COLOR_THEME
} from '../constants/colorThemeActionTypes';

export const setColorTheme = (theme) => {
  return (dispatch) => {
    dispatch({
      type: SET_COLOR_THEME,
      payload: {theme: theme}
    })
  }
};
