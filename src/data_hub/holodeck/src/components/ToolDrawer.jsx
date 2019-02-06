import React from 'react';
import { MDCDrawer } from "@material/drawer";

import CollectionFilterContainer from '../containers/CollectionFilterContainer';
import CollectionSorterContainer from '../containers/CollectionSorterContainer';
import CollectionTimesliderContainer from '../containers/CollectionTimesliderContainer';

import ShareButtons from './DialogTemplateListItems/ShareButtons';

import ThemeChooserContainer from '../containers/ThemeChooserContainer';

export default class ToolDrawer extends React.Component {

  constructor(props) {
      super(props);
      this.clearAllFilters = this.clearAllFilters.bind(this);
  }

  componentDidMount() {
    this.toolDrawer = MDCDrawer.attachTo(document.querySelector('.tool-drawer'));
    if (this.props.view === 'modal') {
      this.props.closeToolDrawer();
    }
  }

  clearAllFilters() {
    this.props.sortNew();
    this.props.setCollectionFilter({});
    this.props.setCollectionFilterMapAoi({});
    this.props.setCollectionFilterMapCenter({lng: -99.341389, lat: 31.33}); // the center of Texas
    this.props.setCollectionFilterMapFilter([]);
    this.props.setCollectionFilterMapZoom(5.8);
    this.props.setCollectionTimeslider(this.props.collectionTimesliderRange);
    this.props.setUrl('/', this.props.history);
    this.props.logFilterChange('/');
  }

  render() {
    console.log(this.props);
    const drawerTypeClass = this.props.view === 'dismiss' ?
      'mdc-drawer mdc-drawer--dismissible tool-drawer' : 'mdc-drawer mdc-drawer--modal tool-drawer';
    const openClass = this.props.toolDrawerStatus === 'open' && this.props.showToolDrawerInCatalogView ?
      'mdc-drawer--open' : '';

    return (
      <div className='tool-drawer-component mdc-typography'>
        <aside className={`${drawerTypeClass} ${openClass}`} dir='rtl'>
          <div className='mdc-drawer__content' dir='ltr'>

              <div className='mdc-drawer__header no-scroll'>
                <div className='dataset-counter'>
                  <span className="dataset-counter-count">{this.props.total}</span> Datasets Found
                </div>
              </div>

            <nav className='mdc-list-group scroll'>
              <div className='sort-title mdc-list-group__subheader'>
                Sort
              </div>
              <CollectionSorterContainer
                className='mdc-list-item'
                match={this.props.match}
                history={this.props.history} />
              <div className='filter-title mdc-list-group__subheader'>
                Filter
              </div>
              <CollectionFilterContainer
                className='mdc-list-item'
                match={this.props.match}
                history={this.props.history} />
              <div className='timeslider-title mdc-list-group__subheader'>
                Date Range
              </div>
              <CollectionTimesliderContainer
                className='mdc-list-item'
                match={this.props.match}
                history={this.props.history} />
              <div className='clear-all-filters-container'>
                <button
                  className="mdc-button mdc-button--raised"
                  onClick={this.clearAllFilters}>
                  Clear All Filters
                </button>
              </div>
              <ThemeChooserContainer />
              <ShareButtons />
            </nav>

          </div>
        </aside>

        {this.props.view === 'modal' ? <div className='mdc-drawer-scrim' id='scrim'></div> : null}

      </div>
    );
  }
}
