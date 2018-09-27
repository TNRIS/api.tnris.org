import React from 'react';
import { MDCDrawer } from "@material/drawer";

import CollectionFilterContainer from '../containers/CollectionFilterContainer';
import CollectionSorterContainer from '../containers/CollectionSorterContainer';

export default class ToolDrawer extends React.Component {

  constructor(props) {
      super(props);
      this.handleCloseDrawer = this.handleCloseDrawer.bind(this);
  }

  componentDidMount() {
    this.toolDrawer = MDCDrawer.attachTo(document.querySelector('.tool-drawer'));
  }

  handleCloseDrawer () {
    this.toolDrawer.open = false;
  }

  render() {
    return (
      <div className='tool-drawer-component mdc-typography'>
        <aside className='mdc-drawer mdc-drawer--modal tool-drawer' dir='rtl'>
          <div className='mdc-drawer__content' dir='ltr'>
            <nav className='mdc-list-group'>
              <a className='sort-title mdc-list-group__subheader'>
                Sort
              </a>
              <CollectionSorterContainer className='mdc-list-item' />
              <hr className='mdc-list-divider'/>
              <a className='filter-title mdc-list-group__subheader'>
                Filter
              </a>
              <CollectionFilterContainer className='mdc-list-item' />
            </nav>
          </div>
        </aside>
        <div className='mdc-drawer-scrim'></div>
      </div>
    );
  }
}
