import React from 'react';

export default class CollectionFilter extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      filters: this.props.collectionFilter
    }
    this.handleOpenFilterMenu = this.handleOpenFilterMenu.bind(this);
    this.handleSetFilter = this.handleSetFilter.bind(this);
  }

  componentDidMount() {
    this.props.setCollectionFilter(this.props.collectionFilterChoices);
  }

  handleOpenFilterMenu(e) {
    let filterName = e.target.id.split('-')[0];
    let filterListElement = document.getElementById(`${filterName}-list`);
    let filterListTitleIcon = document.getElementById(`${filterName}-expansion-icon`);

    filterListElement.classList.contains('hide-filter-list') ?
      filterListElement.classList.remove('hide-filter-list') :
      filterListElement.classList.add('hide-filter-list');

    filterListTitleIcon.innerHTML === 'expand_more' ?
      filterListTitleIcon.innerHTML = 'expand_less' :
      filterListTitleIcon.innerHTML = 'expand_more';
  }

  handleSetFilter(target) {
    let currentFilters = {...this.props.collectionFilter};

    if (target.checked) {
      if (currentFilters.hasOwnProperty(target.name) && currentFilters[target.name].indexOf(target.value) < 0) {
        currentFilters[target.name].push(target.value);
      } else {
        currentFilters[target.name] = [target.value];
      }
      this.props.setCollectionFilter(currentFilters);
    } else {
      if (currentFilters.hasOwnProperty(target.name) && currentFilters[target.name].indexOf(target.value) >= 0) {
        currentFilters[target.name] = currentFilters[target.name].filter(item => item !== target.value)
      }
      this.props.setCollectionFilter(currentFilters);
    }
  }

  render() {
    console.log(this.props);
    return (
      <div className='filter-component'>
        <ul className='mdc-list'>
          <li key='filter-map-button'>
            <a
              className='mdc-list-item filter-list-title'
              id='filter-map-button'
              onClick={this.props.openCollectionFilterMapDialog}>
              by geography
            </a>
          </li>
          {
            Object.keys(this.props.collectionFilterChoices).map(choice =>
              <li key={choice}>
                <a
                  className='mdc-list-item filter-list-title'
                  id={`${choice}-title`}
                  onClick={e => this.handleOpenFilterMenu(e)}>
                  {`by ${choice.replace(/_/, ' ')}`}
                  <i
                    className='mdc-list-item__meta material-icons'
                    id={`${choice}-expansion-icon`}>expand_more</i>
                </a>
                  <ul className='mdc-list hide-filter-list' id={`${choice}-list`}>
                    {
                      this.props.collectionFilterChoices[choice].map((choiceValue, i) =>
                      <li
                        className='mdc-list-item'
                        key={choiceValue}>
                        <div className='mdc-form-field'>
                          <div className='mdc-checkbox'>
                            <input type='checkbox'
                                   className='mdc-checkbox__native-control'
                                   id={choiceValue}
                                   name={choice}
                                   value={choiceValue}
                                   onChange={e => this.handleSetFilter(e.target)}
                                   defaultChecked/>
                            <div className='mdc-checkbox__background'>
                              <svg className='mdc-checkbox__checkmark'
                                   viewBox='0 0 24 24'>
                                <path className='mdc-checkbox__checkmark-path'
                                      fill='none'
                                      d='M1.73,12.91 8.1,19.28 22.79,4.59'/>
                              </svg>
                              <div className='mdc-checkbox__mixedmark'></div>
                            </div>
                          </div>
                          <label htmlFor={choiceValue}>{choiceValue}</label>
                        </div>
                      </li>)}
                  </ul>
              </li>
            )
          }
        </ul>
      </div>
    );
  }
}
