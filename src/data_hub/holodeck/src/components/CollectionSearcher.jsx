import React from 'react';
import { MDCTextField } from '@material/textfield';

export default class CollectionSearcher extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      searchQuery: this.props.collectionSearchQuery
    }
    this.handleSearch = this.handleSearch.bind(this);
  }

  componentDidMount() {
    this.searchField = new MDCTextField(document.querySelector('.search-component'));
  }

  handleSearch() {
    this.props.setCollectionSearchQuery(this.searchField.value);
  }

  render() {
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
