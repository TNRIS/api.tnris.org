import React from 'react';
import Downshift from 'downshift';
import {MDCList} from '@material/list';
import {MDCMenu} from '@material/menu';
import {MDCMenuSurface} from '@material/menu-surface';
import {MDCRipple} from '@material/ripple';
import { MDCTextField } from '@material/textfield';
import { Redirect } from 'react-router';

const searchFieldBackgroundColor = '#efefef';

export default class CollectionSearcher extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      badUrlFlag: false,
      searchFieldValue: '',
      showSuggestionList: false
    }
    // this.handleSearch = this.handleSearch.bind(this);
    this.handleClearSearch = this.handleClearSearch.bind(this);
    this.updateUrl = this.updateUrl.bind(this);
    this.handleBlur = this.handleBlur.bind(this);
    this.handleFocus = this.handleFocus.bind(this);
    this.handleStateChange = this.handleStateChange.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleKeyUp = this.handleKeyUp.bind(this);
    this.handleSelect = this.handleSelect.bind(this);
  }

  componentDidMount() {
    this.searchField = new MDCTextField(document.querySelector('.search-component'));
    this.searchFieldInput = document.querySelector('.mdc-text-field__input');
    this.searchFieldInput.style.backgroundColor = searchFieldBackgroundColor;
    // this.list = new MDCList(document.querySelector('.mdc-list'));
    // this.list.singleSelection = true;
    // this.listItemRipples = this.list.listElements.map((listItemEl) => new MDCRipple(listItemEl));

    // on component mount, check the URl to apply any necessary filters
    // first, check if url has a 'filters' parameter
    if (Object.keys(this.props.match.params).includes('filters')) {
      try {
        const allFilters = JSON.parse(decodeURIComponent(this.props.match.params.filters));
        // second, check if filters param includes search key
        if (Object.keys(allFilters).includes('search')) {
          // third, apply search text and then populate the input box
          this.props.setCollectionSearchQuery(allFilters.search);
          this.props.setCollectionSearchSuggestionsQuery(allFilters.search);
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

  updateUrl(searchFieldValue) {
    // update URL to reflect new search change
    const prevFilter = this.props.history.location.pathname.includes('/catalog/') ?
                       JSON.parse(decodeURIComponent(this.props.history.location.pathname.replace('/catalog/', '')))
                       : {};
    const filterObj = {...prevFilter, search: searchFieldValue};
    // if search is empty, remove from the url
    if (filterObj['search'].length === 0) {
      delete filterObj['search'];
    }
    const filterString = JSON.stringify(filterObj);
    // if empty filter settings, use the base home url instead of the filter url
    Object.keys(filterObj).length === 0 ? this.props.setUrl('/', this.props.history) : this.props.setUrl('/catalog/' + encodeURIComponent(filterString), this.props.history);
  }

  handleBlur() {
    this.searchField.foundation_.adapter_.removeClass('shadowy');
    this.searchFieldInput.style.backgroundColor = searchFieldBackgroundColor;
    this.setState({showSuggestionList: false});
  }

  handleFocus(event) {
    this.searchField.foundation_.adapter_.addClass('shadowy');
    this.searchFieldInput.style.backgroundColor = 'white';
    if (event.target.value) {
      this.setState({showSuggestionList: true});
    }
  }

  // handleSearch(e) {
  //   try {
  //     if (this.searchField.value) {
  //       // first set the collectionSearchSuggestionsQuery in the app state then set the
  //       // local state for the clear button handling to show the suggestion list
  //       this.props.setCollectionSearchSuggestionsQuery(this.searchField.value);
  //       this.setState({
  //         // searchFieldValue: this.searchField.value,
  //         showSuggestionList: true
  //       });
  //       // we check if the user pressed the enter or escape key
  //       if (e.keyCode === 13) { // they pressed enter, so fire the search
  //           e.preventDefault(); // ensure it is only our code that is run
  //           this.props.setCollectionSearchQuery(this.searchField.value);
  //           this.updateUrl(this.searchField.value);
  //           this.setState({showSuggestionList: false});
  //           this.searchFieldInput.blur();
  //       } else if (e.keyCode === 27) { // they pressed escape, so drop focus
  //         // this.searchFieldInput.blur();
  //       }
  //     } else {
  //       if (e.keyCode === 13) { // they pressed enter, so fire the search
  //         this.props.setCollectionSearchQuery('');
  //         this.props.setCollectionSearchSuggestionsQuery('');
  //         this.updateUrl('');
  //         this.setState({
  //           // searchFieldValue: null,
  //           showSuggestionList: false
  //         });
  //         this.searchFieldInput.blur();
  //       }
  //       if (e.keyCode === 27) { // they pressed escape, so drop focus
  //         this.searchFieldInput.blur();
  //         this.setState({
  //           // searchFieldValue: null,
  //           showSuggestionList: false
  //         });
  //       }
  //       this.props.setCollectionSearchSuggestionsQuery('');
  //       this.setState({
  //         // searchFieldValue: null,
  //         showSuggestionList: false
  //       });
  //     }
  //   } catch(e) {
  //     console.log(e);
  //   }
  // }
  //

  handleInputChange(event) {
    try {
      if (event.target.value) {
        this.setState({searchFieldValue: event.target.value, showSuggestionList: true});
        this.props.setCollectionSearchSuggestionsQuery(event.target.value);
      } else {
        this.setState({searchFieldValue: '', showSuggestionList: false});
        this.props.setCollectionSearchSuggestionsQuery('');
      }
    } catch(e) {
      console.log(e);
    }
  }

  handleKeyUp(event) {
    try {
      // we check if the user pressed the enter or escape key
      if (event.keyCode === 13) { // they pressed enter, so fire the search
        event.preventDefault(); // ensure it is only our code that is run
        this.props.setCollectionSearchQuery(event.target.value);
        this.updateUrl(event.target.value);
        this.setState({showSuggestionList: false});
        event.target.blur();
      } else if (event.keyCode === 27) { // they pressed escape, so drop focus
        event.target.blur();
      }
    } catch(e) {
      console.log(e);
    }
  }

  handleClearSearch() {
    try {
      this.setState({searchFieldValue: ''});
      // this.props.setCollectionSearchQuery('');
      // this.props.setCollectionSearchSuggestionsQuery('');
      // this.updateUrl('');
      this.searchFieldInput.focus();
    } catch(e) {
      console.log(e);
    }
  }

  handleSelect(selection) {
    console.log(selection);
    this.setState({searchFieldValue: selection});
  }

  handleStateChange = (changes, downshiftState) => {
    console.log(changes, downshiftState);

  }

  // handleClearSearch(e) {
  //   try {
  //     if (this.searchField.value) {
  //       // document.getElementById("search-collections").value = '';
  //       this.props.setCollectionSearchQuery('');
  //       this.props.setCollectionSearchSuggestionsQuery('');
  //       this.updateUrl('');
  //       this.setState({
  //         // searchFieldValue: null,
  //         showSuggestionList: false
  //       });
  //       this.searchFieldInput.focus();
  //     }
  //   } catch(e) {
  //     console.log(e);
  //   }
  // }

  // <div
  //   id="searchparent"
  //   className={`search-component mdc-text-field mdc-text-field--fullwidth
  //     mdc-text-field--with-leading-icon mdc-text-field--with-trailing-icon mdc-menu-surface--anchor`}>
  //   <i id="search-icon" className="material-icons mdc-text-field__icon">search</i>
  //   <input className='mdc-text-field__input'
  //          type='search'
  //          id='search-collections'
  //          name='q'
  //          onClick={this.click}
  //          onKeyUp={this.handleSearch}
  //          onFocus={this.handleFocus}
  //          onBlur={this.handleBlur}
  //          placeholder='Search'
  //          aria-label='Search data collections'
  //          tabIndex="0"
  //          autoComplete="off">
  //   </input>
  //   {this.props.collectionSearchSuggestionsQuery ?
  //     <button
  //       id='clear-icon'
  //       className="mdc-icon-button material-icons mdc-text-field__icon"
  //       tabIndex="0"
  //       onClick={this.handleClearSearch}>
  //       clear
  //     </button> : ''}
  //     {this.state.showSuggestionList && this.props.collectionSearchSuggestions.length > 0 ?
  //       <div className="suggestion-list--container">
  //         <ul id="suggestion-list" className="mdc-list" role="listbox">
  //         {this.props.collectionSearchSuggestions.slice(0,5).map(suggestion =>
  //           <li className="mdc-list-item" key={suggestion} role="option">
  //             <span className="mdc-list-item__text">{suggestion}</span>
  //           </li>
  //         )}
  //         </ul>
  //       </div> : ''}
  // </div>
  //
  //
  // onChange={selection => alert(`You selected ${selection}`)}

  render() {
    if (this.state.badUrlFlag) {
      return <Redirect to='/404' />;
    }

    // if (this.searchField) {
    //   if (document.querySelector('.mdc-text-field__input') === document.activeElement) {
    //     this.searchField.foundation_.adapter_.addClass('shadowy');
    //     this.searchFieldInput.style.backgroundColor = 'white';
    //   } else {
    //     this.searchField.foundation_.adapter_.removeClass('shadowy');
    //     this.searchFieldInput.style.backgroundColor = 'grey';
    //   }
    // }
    console.log(this.state);
    console.log(this.props);
    return (
      <Downshift
        onStateChange={this.handleStateChange}
        onChange={selection => this.handleSelect(selection)}
        itemToString={item => (item ? item.value : '')}
      >
        {({
          getInputProps,
          getItemProps,
          getLabelProps,
          getMenuProps,
          isOpen,
          inputValue,
          clearSelection,
          reset,
          highlightedIndex,
          selectedItem,
        }) => (
          <div
            id="searchparent"
            className={`search-component mdc-text-field mdc-text-field--fullwidth
              mdc-text-field--with-leading-icon mdc-text-field--with-trailing-icon mdc-menu-surface--anchor`}>
            <i id="search-icon" className="material-icons mdc-text-field__icon">search</i>
            <input
              className="downshift-input mdc-text-field__input"
              id="search-collections"
              {...getInputProps({
              value: this.state.searchFieldValue,
              placeholder: "Search",
              onChange: this.handleInputChange,
              onKeyUp: this.handleKeyUp,
              onFocus: this.handleFocus,
              onBlur: this.handleBlur
            })}>
            </input>
            {this.props.collectionSearchSuggestionsQuery ?
              <button
                id='clear-icon'
                className="mdc-icon-button material-icons mdc-text-field__icon"
                tabIndex="0"
                onClick={this.handleClearSearch}>
                clear
              </button> : ''}
              {this.state.showSuggestionList && this.props.collectionSearchSuggestions.length > 0 ?

                <ul className="suggestion-list downshift-dropdown mdc-list">
                  {this.props.collectionSearchSuggestions.slice(0,5).map((item, index) =>
                    <li
                      className="dropdown-item mdc-list-item"
                      {...getItemProps({ key: index, index, item })}
                            style={{
                              backgroundColor: highlightedIndex === index ? 'lightgray' : 'white',
                              fontWeight: selectedItem === item ? 'bold' : 'normal',
                            }}>
                      {item}
                    </li>
                  )}
                </ul> : null}
          </div>
        )}
      </Downshift>
    );
  }
}
