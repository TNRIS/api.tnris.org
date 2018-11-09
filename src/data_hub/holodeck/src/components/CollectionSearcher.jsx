import React from 'react';
import { MDCTextField } from '@material/textfield';
import { Redirect } from 'react-router';

export default class CollectionSearcher extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      searchQuery: this.props.collectionSearchQuery,
      badUrlFlag: false
    }
    this.handleSearch = this.handleSearch.bind(this);
  }

  componentDidMount() {
    this.searchField = new MDCTextField(document.querySelector('.search-component'));

    // on component mount, check the URl to apply any necessary filters
    // first, check if url has a 'filters' parameter
    if (Object.keys(this.props.match.params).includes('filters')) {
      try {
        const allFilters = JSON.parse(decodeURIComponent(this.props.match.params.filters));
        // second, check if filters param includes search key
        if (Object.keys(allFilters).includes('search')) {
          // third, apply search text and then populate the input box
          this.props.setCollectionSearchQuery(allFilters.search);
          document.querySelector('#search-collections').value = allFilters.search;
        }
      } catch (e) {
        console.log(e);
        this.setState({
          badUrlFlag: true
        });
      }
    }
  }

  handleSearch() {
    this.props.setCollectionSearchQuery(this.searchField.value);

    // update URL to reflect new search change
    const prevFilter = this.props.history.location.pathname.includes('/catalog/') ?
                       JSON.parse(decodeURIComponent(this.props.history.location.pathname.replace('/catalog/', '')))
                       : {};
    const filterObj = {...prevFilter, search: this.searchField.value};
    // if search is empty, remove from the url
    if (filterObj['search'].length === 0) {
      delete filterObj['search'];
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
      <div className='search-component mdc-text-field mdc-text-field--fullwidth'>
        <input className='mdc-text-field__input'
               type='search'
               id='search-collections'
               name='q'
               onChange={this.handleSearch}
               placeholder='Search'
               aria-label='Search data collections'>
         </input>
      </div>
    );
  }
}
