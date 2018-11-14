import React from 'react';
import { Redirect } from 'react-router';

export default class CollectionFilter extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      badUrlFlag: false
    }
    this.handleOpenFilterMenu = this.handleOpenFilterMenu.bind(this);
    this.handleSetFilter = this.handleSetFilter.bind(this);
  }

  componentDidMount () {
    // on component mount, check the URl to apply any necessary filters
    // first, check if url has a 'filters' parameter
    if (Object.keys(this.props.match.params).includes('filters')) {
      try {
        const allFilters = JSON.parse(decodeURIComponent(this.props.match.params.filters));
        // second, check if filters param includes filters key
        if (Object.keys(allFilters).includes('filters')) {
          // third, apply all filters and check those associated checkboxes
          this.props.setCollectionFilter(allFilters.filters);
          Object.keys(allFilters.filters).map(key => {
            allFilters.filters[key].map(id => {
              const hashId = '#' + id;
              if (document.querySelector(hashId)) {
                document.querySelector(hashId).checked = true;
                document.querySelector(`${hashId}-label`).classList.add('filter-active');
              }
              return hashId;
            });
            return key;
          });
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
    if (Object.keys(nextProps.collectionFilter).length === 0) {
      const filterComponent = document.getElementById('filter-component');
      const inputArray = filterComponent.querySelectorAll("input");
      inputArray.forEach(input => {
        return input.checked = false;
      });
      const groupArray = filterComponent.querySelectorAll("ul[id$='-list']");
      groupArray.forEach(group => {
        if (!group.classList.contains('hide-filter-list')) {
          group.classList.add('hide-filter-list');
        }
        return group;
      });
      const iconArray = filterComponent.querySelectorAll("i[id$='-expansion-icon']");
      iconArray.forEach(icon => {
        if (icon.innerHTML === 'expand_less') {
          icon.innerHTML = 'expand_more';
        }
        return icon;
      });
    }
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
      document.getElementById(`${target.value}-label`).classList.add("filter-active");
    } else {
      if (currentFilters.hasOwnProperty(target.name) && currentFilters[target.name].indexOf(target.value) >= 0) {
        currentFilters[target.name] = currentFilters[target.name].filter(item => item !== target.value);
        // if all checkboxes unchecked, remove from the category's filter object completely
        if (currentFilters[target.name].length === 0) {
          delete currentFilters[target.name];
        }
      }
      this.props.setCollectionFilter(currentFilters);
      document.getElementById(`${target.value}-label`).classList.remove("filter-active");
    }

    // update URL to reflect new filter changes
    const prevFilter = this.props.history.location.pathname.includes('/catalog/') ?
                       JSON.parse(decodeURIComponent(this.props.history.location.pathname.replace('/catalog/', '')))
                       : {};
    const filterObj = {...prevFilter, filters: currentFilters};
    // if all filters turned off, remove from the url completely
    if (Object.keys(filterObj['filters']).length === 0) {
      delete filterObj['filters'];
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
      <div id='filter-component' className='filter-component'>
        <ul className='mdc-list'>
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
                      this.props.collectionFilterChoices[choice].map((choiceValue, i) =>{
                        const labelValue = choiceValue.replace(/_/g, ' ');
                        return (<li
                          className='mdc-list-item'
                          key={choiceValue}>
                          <div className='mdc-form-field'>
                            <div className='mdc-checkbox'>
                              <input type='checkbox'
                                     className='mdc-checkbox__native-control'
                                     id={choiceValue}
                                     name={choice}
                                     value={choiceValue}
                                     onChange={e => this.handleSetFilter(e.target)}/>
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
                            <label id={`${choiceValue}-label`}
                                   htmlFor={choiceValue}>
                                   {labelValue}
                           </label>
                          </div>
                        </li>);
                    })}
                  </ul>
              </li>
            )
          }
          <li key='filter-map-button'>
            <a className='mdc-list-item filter-list-title'
               id='filter-map-button'
               onClick={this.props.openCollectionFilterMapDialog}>
               by geography
            </a>
          </li>
        </ul>
      </div>
    );
  }
}
