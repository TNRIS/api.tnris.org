import React, { Component } from 'react';

class ThemeChooser extends Component {
  constructor(props) {
      super(props);
      this.setColorTheme = this.setColorTheme.bind(this);
      this.themeOptions = ['light', 'earth'];
  }

  componentDidMount() {
    // on component mount, check localstorage for theme to apply
    if (typeof(Storage) !== void(0)) {
      const savedTheme = localStorage.getItem("data_theme") ? localStorage.getItem("data_theme") : null;
      if (savedTheme) {
        if (this.themeOptions.includes(savedTheme)) {
          this.setColorTheme(savedTheme);
        }
        else {
          localStorage.removeItem("data_theme");
        }
      }
    }
  }

  setColorTheme(theme) {
    this.props.setColorTheme(theme);
  }

  render() {
    return (
      <div className="theme-chooser-component">
        {this.themeOptions.map(theme => {
          const label = theme.charAt(0).toUpperCase() + theme.slice(1);
          const themeClass = `theme-chooser-option ${theme}-app-theme`;
          return <div key={theme}
                      onClick={() => this.setColorTheme(theme)}
                      className={themeClass}
                      title={label}></div>
        })}
      </div>
    )
  }
}

export default ThemeChooser
