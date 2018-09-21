import React from 'react';

import { MDCCheckbox } from '@material/checkbox';
import { MDCFormField } from '@material/form-field';
import { MDCMenu } from '@material/menu';

export default class CollectionFilter extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      filter: false
    }
    this.handleSetFilter = this.handleSetFilter.bind(this);
    this.showFilterMenu = this.showFilterMenu.bind(this);
    this.showNestedMenu = this.showNestedMenu.bind(this);
  }

  componentDidMount() {
    this.menu = new MDCMenu(this.refs.filter_menu);
    // const menu = new MDCMenu(document.querySelector('.mdc-menu'));
    // const checkboxEls = Array.from(document.querySelectorAll('.mdc-checkbox'));
    // const formFieldEls = Array.from(document.querySelectorAll('.mdc-form-field'));
    // // formField.input = checkbox;
    // console.log(checkboxEls);
    // console.log(formFieldEls);
    // console.log(this.menu.items);
    // this.menu.open = true;
  }

  showFilterMenu() {
    this.menu.open = true;
  }

  showNestedMenu() {
    console.log("clicked");
  }

  handleSetFilter() {
    this.setState({filter: !this.state.filter}, () => {
      if (this.state.filter) {
        this.props.setCollectionFilter({
          category: 'Environmental',
          recommended_use: 'General Large Scale Geologic Information and Mapping'
        });
      } else {
        this.props.setCollectionFilter({});
      }
    });
  }

  render() {
    console.log(this.props);
    return (
      <div className='filter-component mdc-menu-surface--anchor'>
        <button onClick={this.showFilterMenu} className='filter-button mdc-button mdc-button--raised'>
          filter
        </button>
        {/* <div ref='filter_menu' className='mdc-menu mdc-menu-surface'>
          <ul className='mdc-list mdc-menu__items' role='menu' aria-hidden='true'> */}
          <div ref='filter_menu' className='mdc-menu mdc-menu-surface'>
            <ul className='mdc-list-group mdc-menu__items' role='menu' aria-hidden='true'>
            {
              Object.keys(this.props.collectionFilterChoices).map(choice =>
                <li key={choice} role='menuitem'>
                  <h4 className='mdc-list-group__subheader mdc-list-item__text'>{choice.replace(/_/, ' ')}</h4>
                  <hr className='mdc-list-divider'/>
                  <ul className='mdc-list'>
                    {
                      this.props.collectionFilterChoices[choice].map((choiceValue, i) =>
                        <li
                          className='mdc-list-item'
                          key={choiceValue}>
                          <div className="mdc-form-field">
                            <div className="mdc-checkbox">
                              <input type="checkbox"
                                     className="mdc-checkbox__native-control"
                                     id={`checkbox-${i}`}/>
                              <div className="mdc-checkbox__background">
                                <svg className="mdc-checkbox__checkmark"
                                     viewBox="0 0 24 24">
                                  <path className="mdc-checkbox__checkmark-path"
                                        fill="none"
                                        d="M1.73,12.91 8.1,19.28 22.79,4.59"/>
                                </svg>
                                <div className="mdc-checkbox__mixedmark"></div>
                              </div>
                            </div>
                            <label htmlFor={`checkbox-${i}`}>{choiceValue}</label>
                          </div>
                        </li>
                      )
                    }
                  </ul>
                </li>
              )
            }
            {/* {
              Object.keys(this.props.collectionFilterChoices).map(choice =>
              <li
                className='mdc-list-item'
                key={choice}
                role='menuitem'
                onClick={this.showNestedMenu}>
                <span className='mdc-list-item__text'>{choice.replace(/_/, ' ')}</span>
              </li>
              )
            } */}
          </ul>
        </div>
      </div>
    );
  }
}
