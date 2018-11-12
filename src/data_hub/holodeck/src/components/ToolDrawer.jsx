import React from 'react';
import { MDCDrawer } from "@material/drawer";

import CollectionFilterContainer from '../containers/CollectionFilterContainer';
import CollectionSearcherContainer from '../containers/CollectionSearcherContainer';
import CollectionSorterContainer from '../containers/CollectionSorterContainer';
import CollectionTimesliderContainer from '../containers/CollectionTimesliderContainer';

export default class ToolDrawer extends React.Component {

  constructor(props) {
      super(props);

      // let deviceWidth = window.innerWidth;

      if (window.innerWidth >= 1000){
        this.state = {
          view: 'dismiss'
        };
      }
      else {
        this.state = {
          view: 'modal'
        };
      }

      console.log(this.state.view, window.innerWidth);

      this.handleCloseDrawer = this.handleCloseDrawer.bind(this);

  }

  componentDidMount() {
    this.toolDrawer = MDCDrawer.attachTo(document.querySelector('.tool-drawer'));
  }

  handleCloseDrawer() {
    this.toolDrawer.open = false;
  }

  render() {
    let classname = 'mdc-drawer mdc-drawer--modal tool-drawer';
    // console.log(this.state.view);

    window.addEventListener("resize", function() {
      // console.log(window.innerWidth);
      // if (this.state.view === 'dismiss') {
      //   classname = 'mdc-drawer mdc-drawer--dismissible tool-drawer';
      // }
      console.log('resize is happening!!!', this.state.view);
    });

    return (

      <div className='tool-drawer-component mdc-typography'>
        <aside className={classname} dir='rtl'>
          <div className='mdc-drawer__content' dir='ltr'>
            <nav className='mdc-list-group'>
              <CollectionSearcherContainer className='mdc-list-item' match={this.props.match} history={this.props.history} />
              <a className='sort-title mdc-list-group__subheader'>
                Sort
              </a>
              <CollectionSorterContainer className='mdc-list-item' match={this.props.match} history={this.props.history} />
              <hr className='mdc-list-divider'/>
              <a className='filter-title mdc-list-group__subheader'>
                Filter
              </a>
              <CollectionFilterContainer className='mdc-list-item' match={this.props.match} history={this.props.history} />
                <hr className='mdc-list-divider'/>
                <a className='timeslider-title mdc-list-group__subheader'>
                  Acquisition Date Range
                </a>
              <CollectionTimesliderContainer className='mdc-list-item' match={this.props.match} history={this.props.history} />
            </nav>
          </div>
        </aside>
        <div className='mdc-drawer-scrim'></div>
      </div>
    );
  }
}
