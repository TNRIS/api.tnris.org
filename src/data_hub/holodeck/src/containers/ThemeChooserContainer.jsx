import { connect } from 'react-redux';

import { colorThemeActions } from '../actions';
import ThemeChooser from '../components/ThemeChooser';

const mapStateToProps = state => ({
  theme: state.colorTheme.theme
});

const mapDispatchToProps = dispatch => ({
  setColorTheme: (theme) => {
    dispatch(colorThemeActions.setColorTheme(theme));
  }
})

const ThemeChooserContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(ThemeChooser);

export default ThemeChooserContainer;
