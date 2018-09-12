import React, { Component } from 'react';
import { MDCMenu } from '@material/menu';

class Sort extends Component {

  constructor(props) {
      super(props);
      this.state = {
        sortOrder: this.props.sortOrder
      }
      this.showSortMenu = this.showSortMenu.bind(this);
      this.setSort = this.setSort.bind(this);
  }

  showSortMenu() {
    const menu = new MDCMenu(this.refs.sort_menu);
    menu.open = true;
  }

  setSort(order) {
    this.setState({sortOrder: order});
    switch(order) {
      case 'AZ':
        this.props.sortAZ();
        break;
      case 'ZA':
        this.props.sortZA();
        break;
      case 'NEW':
        this.props.sortNew();
        break;
      case 'OLD':
        this.props.sortOld();
        break;
      default:
        this.props.sortAZ();
    }
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
      case 'NEW':
        label = 'Newest';
        break;
      case 'OLD':
        label = 'Oldest';
        break;
      default:
        label = 'A to Z';
    }

    return (
      <div className="sort-component mdc-menu-surface--anchor">
        <button onClick={this.showSortMenu} className="mdc-button mdc-button--raised sort-button">
          {label}
        </button>
        <div ref="sort_menu" className="mdc-menu mdc-menu-surface">
          <ul className="mdc-list mdc-menu__items" role="menu" aria-hidden="true">
            <li className={this.state.sortOrder === 'AZ' ? 'mdc-list-item  active' : 'mdc-list-item'} role="menuitem" tabIndex="0" onClick={() => this.setSort("AZ")}>
              A to Z
            </li>
            <li className={this.state.sortOrder === 'ZA' ? 'mdc-list-item  active' : 'mdc-list-item'} role="menuitem" tabIndex="1" onClick={() => this.setSort("ZA")}>
              Z to A
            </li>
            <li className={this.state.sortOrder === 'NEW' ? 'mdc-list-item  active' : 'mdc-list-item'} role="menuitem" tabIndex="1" onClick={() => this.setSort("NEW")}>
              Newest
            </li>
            <li className={this.state.sortOrder === 'OLD' ? 'mdc-list-item  active' : 'mdc-list-item'} role="menuitem" tabIndex="1" onClick={() => this.setSort("OLD")}>
              Oldest
            </li>
          </ul>
        </div>
      </div>
    )
  }
}

export default Sort
