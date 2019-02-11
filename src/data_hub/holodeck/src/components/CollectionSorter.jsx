import React from 'react';
import { Redirect } from 'react-router';
import { matchPath } from 'react-router-dom';
import {MDCList} from '@material/list';

class CollectionSorter extends React.Component {

  constructor(props) {
      super(props);
      this.state = {
        badUrlFlag: false
      }
      this.setSort = this.setSort.bind(this);
      this.handleKeyPress = this.handleKeyPress.bind(this);
  }

  componentDidMount() {
    const list = new MDCList(document.getElementById('sorter-list'));
    list.singleSelection = true;
    // on component mount, check the URl to apply any necessary filters
    // first, check if url has a 'filters' parameter
    const match = matchPath(
        this.props.location.pathname,
        { path: '/catalog/:filters' }
      );
    const filters = match ? match.params.filters : null;
    if (filters) {
      try {
        const allFilters = JSON.parse(decodeURIComponent(filters));
        // second, check if filters param includes sort key
        if (Object.keys(allFilters).includes('sort')) {
          // third, apply sort to store and component
          this.setSort(allFilters.sort);
        }
      } catch (e) {
        console.log(e);
        this.setState({
          badUrlFlag: true
        });
      }
    }
  }

  setSort(order) {
    switch(order) {
      case 'NEW':
        this.props.sortNew();
        break;
      case 'OLD':
        this.props.sortOld();
        break;
      case 'AZ':
        this.props.sortAZ();
        break;
      case 'ZA':
        this.props.sortZA();
        break;
      default:
        this.props.sortNew();
    }
    // update URL to reflect new sort change
    const prevFilter = this.props.history.location.pathname.includes('/catalog/') ?
                       JSON.parse(decodeURIComponent(this.props.history.location.pathname.replace('/catalog/', '')))
                       : {};
    const filterObj = {...prevFilter, sort: order};
    // if the default sort 'NEW' then remove from the url
    if (filterObj['sort'] === 'NEW') {
      delete filterObj['sort'];
    }
    const filterString = JSON.stringify(filterObj);
    // if empty filter settings, use the base home url instead of the filter url
    Object.keys(filterObj).length === 0 ? this.props.setUrl('/') : this.props.setUrl('/catalog/' + encodeURIComponent(filterString));
    // log filter change in store
    Object.keys(filterObj).length === 0 ? this.props.logFilterChange('/') : this.props.logFilterChange('/catalog/' + encodeURIComponent(filterString));
  }

  handleKeyPress (e, order) {
    if (e.keyCode === 13 || e.keyCode === 32) {
      this.setSort(order);
    }
  }

  render() {
    if (this.state.badUrlFlag) {
      return <Redirect to='/404' />;
    }

    return (
      <div className='sort-component'>
          <ul id="sorter-list" className='mdc-list' role="listbox" aria-label="Sort list">
            <li
              id="sorter-list-opt1"
              className={this.props.sortOrder === 'NEW' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
              role="option"
              aria-selected={this.props.sortOrder === 'NEW' ? "true" : "false"}
              tabIndex="0"
              onClick={() => this.setSort("NEW")}
              onKeyDown={(e) => this.handleKeyPress(e, "NEW")}>
               <span className='mdc-list-item__text'>Newest</span>
            </li>
            <li
              id="sorter-list-opt2"
              className={this.props.sortOrder === 'OLD' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
              role="option"
              aria-selected={this.props.sortOrder === 'OLD' ? "true" : "false"}
              onClick={() => this.setSort("OLD")}
              onKeyDown={(e) => this.handleKeyPress(e, "OLD")}>
               <span className='mdc-list-item__text'>Oldest</span>
            </li>
            <li
              id="sorter-list-opt3"
              className={this.props.sortOrder === 'AZ' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
              role="option"
              aria-selected={this.props.sortOrder === 'AZ' ? "true" : "false"}
              onClick={() => this.setSort("AZ")}
              onKeyDown={(e) => this.handleKeyPress(e, "AZ")}>
               <span className='mdc-list-item__text'>A to Z</span>
            </li>
            <li
              id="sorter-list-opt4"
              className={this.props.sortOrder === 'ZA' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
              role="option"
              aria-selected={this.props.sortOrder === 'ZA' ? "true" : "false"}
              onClick={() => this.setSort("ZA")}
              onKeyDown={(e) => this.handleKeyPress(e, "ZA")}>
               <span className='mdc-list-item__text'>Z to A</span>
            </li>
          </ul>
      </div>
    )
  }
}

export default CollectionSorter
