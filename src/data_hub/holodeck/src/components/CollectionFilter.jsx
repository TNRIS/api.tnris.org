import React from 'react';

import { MDCMenu } from '@material/menu';

export default class CollectionFilter extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      filter: false
    }
    this.handleSetFilter = this.handleSetFilter.bind(this);
    this.showFilterMenu = this.showFilterMenu.bind(this);
    this.showNestedMenu = this.showNestedMenu.bind(this);
  }

  componentDidMount() {
    this.menu = new MDCMenu(this.refs.filter_menu);
  }

  showFilterMenu() {
    this.menu.open = true;
  }

  showNestedMenu() {
    console.log("clicked");
  }

  handleSetFilter() {
    this.setState({filter: !this.state.filter}, () => {
      if (this.state.filter) {
        this.props.setCollectionFilter({
          category: 'Environmental',
          recommended_use: 'General Large Scale Geologic Information and Mapping'
        });
      } else {
        this.props.setCollectionFilter({});
      }
    });
  }

  render() {
    return (
      <div className='filter-component mdc-menu-surface--anchor'>
        <button onClick={this.showFilterMenu} className='filter-button mdc-button mdc-button--raised'>
          filter
        </button>
        <div ref='filter_menu' className='mdc-menu mdc-menu-surface'>
          <ul className='mdc-list mdc-menu__items' role='menu' aria-hidden='true'>
            {
              Object.keys(this.props.collectionFilterChoices).map(choice =>
              <li
                className='mdc-list-item'
                key={choice}
                role='menuitem'
                onClick={this.showNestedMenu}>
                <span className='mdc-list-item__text'>{choice.replace(/_/, ' ')}</span>
              </li>
              )
            }
            {/* {
              Object.keys(this.props.collectionFilterChoices).map(choice =>
              <li key={choice}><span className='mdc-list-item__text'>{choice.replace(/_/, ' ')}</span>
                <ul className="mdc-menu__selection-group">
                  <li className="mdc-list-item" role="menuitem"}>
                    <span className="mdc-menu__selection-group-icon material-icons">
                      check
                    </span>
                    <span className="mdc-list-item__text">Single</span>
                  </li>
                  <li className="mdc-list-item" role="menuitem">
                    <span className="mdc-menu__selection-group-icon material-icons">
                      check
                    </span>
                    <span className="mdc-list-item__text">double</span>
                  </li>
                </ul>
              </li>
              )
            } */}
          </ul>
        </div>
      </div>
    );
  }
}
