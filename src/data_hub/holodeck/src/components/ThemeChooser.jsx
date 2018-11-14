import React, { Component } from 'react';

class ThemeChooser extends Component {
  constructor(props) {
      super(props);
      this.setColorTheme = this.setColorTheme.bind(this);
  }

  setColorTheme (theme) {
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
