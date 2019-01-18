import React, { Component } from 'react';

class ThemeChooser extends Component {
  constructor(props) {
      super(props);
      this.setColorTheme = this.setColorTheme.bind(this);
      // this.themeOptions = ['light', 'dark', 'earth', 'fuego', 'vaporwave', 'america', 'hulk', 'relax'];
      this.themeOptions = ['light', 'dark'];
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
          const label = theme.replace("-", " ").replace(/\b\w/g, l => l.toUpperCase());
          const themeClass = `theme-chooser-option ${theme}-app-theme`;
          const checked = this.props.theme === theme ? <i className='material-icons'>done</i> : '';
          return <div key={theme}
                      onClick={() => this.setColorTheme(theme)}
                      className={themeClass}
                      title={label}>{checked}</div>
        })}
      </div>
    )
  }
}

export default ThemeChooser
