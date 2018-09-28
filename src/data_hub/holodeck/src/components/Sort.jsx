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
    this.menu = new MDCMenu(this.refs.sort_menu);
    this.menu.open = true;
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

    return (
      <div className="sort-component mdc-menu-surface--anchor">
        <a onClick={this.showSortMenu} className="mdc-top-app-bar__action-item">
          <i className="material-icons mdc-top-app-bar__navigation-icon">sort_by_alpha</i>
        </a>
        <div ref="sort_menu" className="mdc-menu mdc-menu-surface">
          <nav className="mdc-list">
            <a className={this.state.sortOrder === 'AZ' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
               onClick={() => this.setSort("AZ")}>
               A to Z
            </a>
            <a className={this.state.sortOrder === 'ZA' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
               onClick={() => this.setSort("ZA")}>
               Z to A
            </a>
            <a className={this.state.sortOrder === 'NEW' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
               onClick={() => this.setSort("NEW")}>
               Newest
            </a>
            <a className={this.state.sortOrder === 'OLD' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
               onClick={() => this.setSort("OLD")}>
               Oldest
            </a>
          </nav>
        </div>
      </div>
    )
  }
}

export default Sort
