import React from 'react';
import { MDCDrawer } from "@material/drawer";

import CollectionFilterContainer from '../containers/CollectionFilterContainer';
import CollectionSearcherContainer from '../containers/CollectionSearcherContainer';
import CollectionSorterContainer from '../containers/CollectionSorterContainer';
import CollectionTimesliderContainer from '../containers/CollectionTimesliderContainer';

import ThemeChooserContainer from '../containers/ThemeChooserContainer';

export default class ToolDrawer extends React.Component {

  constructor(props) {
      super(props);
      this.handleCloseDrawer = this.handleCloseDrawer.bind(this);
      this.clearAllFilters = this.clearAllFilters.bind(this);
  }

  componentDidMount() {
    this.toolDrawer = MDCDrawer.attachTo(document.querySelector('.tool-drawer'));
  }

  handleCloseDrawer() {
    this.toolDrawer.open = false;
  }

  clearAllFilters() {
    this.props.setCollectionSearchQuery('');
    this.props.sortAZ();
    this.props.setCollectionFilter({});
    this.props.setCollectionFilterMapAoi({});
    this.props.setCollectionFilterMapCenter({lng: -99.341389, lat: 31.33}); // the center of Texas
    this.props.setCollectionFilterMapFilter([]);
    this.props.setCollectionFilterMapZoom(5.8);
    this.props.setCollectionTimeslider(this.props.collectionTimesliderRange);
    this.props.setUrl('/', this.props.history);
  }

  render() {
    return (
      <div className='tool-drawer-component mdc-typography'>
        <aside className='mdc-drawer mdc-drawer--modal tool-drawer' dir='rtl'>
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
              <hr className='mdc-list-divider'/>
              <div className='clear-all-filters-container'>
                <button className="mdc-button mdc-button--raised" onClick={this.clearAllFilters}>Clear All</button>
              </div>
              <ThemeChooserContainer />
            </nav>
          </div>
        </aside>
        <div className='mdc-drawer-scrim'></div>
      </div>
    );
  }
}
