import React, { Component } from 'react';

class ThemeChooser extends Component {
  constructor(props) {
      super(props);
      this.setColorTheme = this.setColorTheme.bind(this);
      this.themeOptions = ['light', 'green'];
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
          <div onClick={() => this.setColorTheme('light')}
               className="theme-chooser-option light-app-theme">
               purple
          </div>
          <div onClick={() => this.setColorTheme('green')}
               className="theme-chooser-option green-app-theme">
               green
          </div>
      </div>
    )
  }
}

export default ThemeChooser
