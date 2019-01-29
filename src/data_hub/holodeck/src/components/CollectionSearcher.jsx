import React from 'react';
import Downshift from 'downshift';
import { MDCTextField } from '@material/textfield';
import { Redirect } from 'react-router';

export default class CollectionSearcher extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      badUrlFlag: false,
      searchFieldValue: '',
      showSuggestionList: false
    }

    this.handleBlur = this.handleBlur.bind(this);
    this.handleClearSearch = this.handleClearSearch.bind(this);
    this.handleFocus = this.handleFocus.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleKeyUp = this.handleKeyUp.bind(this);
    this.handleSelect = this.handleSelect.bind(this);
    this.updateUrl = this.updateUrl.bind(this);
  }

  componentDidMount() {
    this.searchField = new MDCTextField(document.querySelector('.search-component'));
    this.searchFieldInput = document.querySelector('.mdc-text-field__input');

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
          this.setState({searchFieldValue: allFilters.search});
        }
      } catch (e) {
        console.log(e);
        this.setState({
          badUrlFlag: true
        });
      }
    }
  }

  // if the input loses focus, hide the suggestionList
  handleBlur() {
    this.setState({showSuggestionList: false});
  }

  // if the input gains focus and has value, show the suggestionList
  handleFocus(event) {
    if (event.target.value) {
      this.setState({showSuggestionList: true});
    }
  }

  // clears the text from the search input, resets the local state, and resets
  // the collectionSearchSuggestionsQuery to empty in the app's state
  handleClearSearch() {
    try {
      this.setState({
        searchFieldValue: '',
        showSuggestionList: false
      });
      // this.props.setCollectionSearchQuery('');
      this.props.setCollectionSearchSuggestionsQuery('');
      // this.updateUrl('');
      this.searchFieldInput.focus();
    } catch(e) {
      console.log(e);
    }
  }

  // sets the local state with the input value, shows or hides the suggestionList,
  // and sets the collectionSearchsuggestionsQuery to retrieve search suggestions
  // from the search index
  handleInputChange(event) {
    try {
      if (event.target.value) {
        this.setState({
          searchFieldValue: event.target.value,
          showSuggestionList: true
        });
        this.props.setCollectionSearchSuggestionsQuery(event.target.value);
      } else {
        this.setState({
          searchFieldValue: '',
          showSuggestionList: false
        });
        this.props.setCollectionSearchSuggestionsQuery('');
      }
    } catch(e) {
      console.log(e);
    }
  }

  // handles firing the search if the user presses enter or blurs the input if
  // they press escape while in the search textField
  handleKeyUp(event) {
    try {
      // we check if the user pressed the enter or escape key
      if (event.keyCode === 13) { // they pressed enter, so fire the search
        event.preventDefault(); // ensure it is only our code that is run
        this.props.setCollectionSearchQuery(event.target.value);
        this.updateUrl(event.target.value);
        this.setState({showSuggestionList: false});
        event.target.blur();
        if (this.props.view !== 'catalog') {
          this.props.setViewCatalog();
          this.props.clearSelectedCollection();
          this.props.openToolDrawer();
        }
      } else if (event.keyCode === 27) { // they pressed escape, so drop focus
        event.target.blur();
      }
    } catch(e) {
      console.log(e);
    }
  }

  // handles firing the search if the user selects an item from the suggestionList
  handleSelect(selection) {
    this.setState({
      searchFieldValue: selection,
      showSuggestionList: false
    });
    this.props.setCollectionSearchQuery(selection);
    this.props.setCollectionSearchSuggestionsQuery(selection);
    this.updateUrl(selection);
    this.searchFieldInput.blur();
    if (this.props.view !== 'catalog') {
      this.props.setViewCatalog();
      this.props.clearSelectedCollection();
      this.props.openToolDrawer();
    }

  }

  // updates the url to reflect the current state of the search input textField
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
    Object.keys(filterObj).length === 0 ? this.props.setUrl('/', this.props.history) :
      this.props.setUrl('/catalog/' + encodeURIComponent(filterString), this.props.history);
    // log filter change in store
    Object.keys(filterObj).length === 0 ? this.props.logFilterChange('/') :
      this.props.logFilterChange('/catalog/' + encodeURIComponent(filterString));
}

  render() {
    if (this.state.badUrlFlag) {
      return <Redirect to='/404' />;
    }

    return (
      <Downshift
        onChange={selection => this.handleSelect(selection)}
        itemToString={item => (item ? item.value : '')}
      >
        {({
          getInputProps,
          getItemProps,
          isOpen,
          inputValue,
          highlightedIndex,
          selectedItem,
        }) => (
          <div
            id="searchparent"
            className={`search-component mdc-text-field mdc-text-field--fullwidth
              mdc-text-field--with-leading-icon mdc-text-field--with-trailing-icon mdc-menu-surface--anchor`}>
            <i id="search-icon" className="material-icons mdc-text-field__icon">search</i>
            <input
              className="search-input downshift-input mdc-text-field__input"
              tabIndex="3"
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
                className="clear-button mdc-top-app-bar__action-item material-icons mdc-text-field__icon"
                tabIndex="3"
                onClick={this.handleClearSearch}>
                clear
              </button> : ''}
              {this.state.showSuggestionList && this.props.collectionSearchSuggestions !== undefined &&
                this.props.collectionSearchSuggestions.length !== 0 ?
                <ul className="suggestion-list downshift-dropdown mdc-list">
                  {this.props.collectionSearchSuggestions.slice(0,5).map((item, index) =>
                    <li
                      className="dropdown-item mdc-list-item"
                      {...getItemProps({ key: index, index, item })}
                            style={{
                              backgroundColor: highlightedIndex === index ? 'lightgray' : 'white',
                              // fontWeight: selectedItem === item ? 'bold' : 'normal',
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
