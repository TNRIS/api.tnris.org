import React from 'react';
import { MDCTextField } from '@material/textfield';

export default class CollectionSearcher extends React.Component {

  constructor(props) {
    super(props);
  }

  componentDidMount() {
    this.searchField = new MDCTextField(document.querySelector('.search-component'));
  }

  render() {
    return (
      <div className='search-component mdc-text-field mdc-text-field--fullwidth'>
        <input className='mdc-text-field__input'
               type='search'
               id='search-collections'
               placeholder='Search'
               aria-label='Full-Width Text Field'>
         </input>
      </div>
    );
  }
}
