import React, { Component } from 'react';
import { MDCMenu } from '@material/menu';

class Sort extends Component {

  constructor(props) {
      super(props);
      this.state = {
        sortOrder: this.props.sortOrder
      }
      console.log(this.state);
  }

  showSortMenu() {
    console.log(document.querySelector('.mdc-menu'));
    const menu = new MDCMenu(document.querySelector('.mdc-menu'));
    console.log(menu);
    menu.open = true;
  }

  render() {
    let label;
    switch(this.state.sortOrder) {
      case 'AZ':
        label = 'A to Z';
        break;
      case 'ZA':
        label = 'Z to A';
        break;
      default:
        label = 'A to Z';
    }

    return (
      <div className="sort-component">
        <button id="menu-button" onClick={this.showSortMenu} className="mdc-button mdc-button--raised sort-button">{label}</button>
        <div className="mdc-menu mdc-menu-surface">
          <ul className="mdc-list mdc-menu__items" role="menu" aria-hidden="true">
            <li className="mdc-list-item" role="menuitem" tabIndex="0">
              A Menu Item
            </li>
            <li className="mdc-list-item" role="menuitem" tabIndex="0">
              Another Menu Item
            </li>
          </ul>
        </div>
      </div>
    )
  }
}

export default Sort
