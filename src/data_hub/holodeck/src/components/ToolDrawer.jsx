import React from 'react';
import { MDCDrawer } from "@material/drawer";

import CollectionFilterContainer from '../containers/CollectionFilterContainer';
import CollectionSearcherContainer from '../containers/CollectionSearcherContainer';
import CollectionSorterContainer from '../containers/CollectionSorterContainer';
import CollectionTimesliderContainer from '../containers/CollectionTimesliderContainer';

export default class ToolDrawer extends React.Component {

  constructor(props) {
      super(props);

      // set initial state view
      this.state = {view: 'dismiss'};
      window.innerWidth >= 1052 ? this.state = {view:'dismiss'} : this.state = {view: 'modal'};

      this.handleCloseDrawer = this.handleCloseDrawer.bind(this);
      this.handleResize = this.handleResize.bind(this);
  }

  handleResize() {
    window.innerWidth >= 1052 ? this.setState({view:'dismiss'}) : this.setState({view:'modal'});
  }

  componentDidMount() {
    this.toolDrawer = MDCDrawer.attachTo(document.querySelector('.tool-drawer'));
    window.addEventListener("resize", this.handleResize);
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this.handleResize);
  }

  handleCloseDrawer() {
    this.toolDrawer.open = false;
  }

  render() {
    let classname;

    this.state.view === 'dismiss' ? classname = 'mdc-drawer mdc-drawer--dismissible tool-drawer' : classname = 'mdc-drawer mdc-drawer--modal tool-drawer';

    return (

      <div className='tool-drawer-component mdc-typography'>
        <aside className={classname} dir='rtl'>
          <div className='mdc-drawer__content' dir='ltr'>
            <nav className='mdc-list-group'>
              <div className='dataset-counter'>
                Showing <span className="dataset-counter-count">{this.props.total}</span> Datasets
              </div>
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
