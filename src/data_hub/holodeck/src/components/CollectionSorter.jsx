import React from 'react';
import { Redirect } from 'react-router';

class CollectionSorter extends React.Component {

  constructor(props) {
      super(props);
      this.state = {
        sortOrder: this.props.sortOrder,
        badUrlFlag: false
      }
      this.setSort = this.setSort.bind(this);
  }

  componentDidMount() {
    // on component mount, check the URl to apply any necessary filters
    // first, check if url has a 'filters' parameter
    if (Object.keys(this.props.match.params).includes('filters')) {
      try {
        const allFilters = JSON.parse(decodeURIComponent(this.props.match.params.filters));
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

  componentWillReceiveProps(nextProps) {
      if (nextProps.sortOrder === 'NEW') {
        this.setState({sortOrder: 'NEW'});
      }
  }

  setSort(order) {
    this.setState({sortOrder: order});
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
    Object.keys(filterObj).length === 0 ? this.props.setUrl('/', this.props.history) : this.props.setUrl('/catalog/' + encodeURIComponent(filterString), this.props.history);
  }

  render() {
    if (this.state.badUrlFlag) {
      return <Redirect to='/404' />;
    }

    return (
      <div className='sort-component'>
          <ul className='mdc-list'>
            <li
              className={this.state.sortOrder === 'NEW' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
              onClick={() => this.setSort("NEW")}>
               <span className='mdc-list-item__text'>Newest</span>
            </li>
            <li
              className={this.state.sortOrder === 'OLD' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
              onClick={() => this.setSort("OLD")}>
               <span className='mdc-list-item__text'>Oldest</span>
            </li>
            <li
              className={this.state.sortOrder === 'AZ' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
              onClick={() => this.setSort("AZ")}>
               <span className='mdc-list-item__text'>A to Z</span>
            </li>
            <li
              className={this.state.sortOrder === 'ZA' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
              onClick={() => this.setSort("ZA")}>
               <span className='mdc-list-item__text'>Z to A</span>
            </li>
          </ul>
      </div>
    )
  }
}

export default CollectionSorter
