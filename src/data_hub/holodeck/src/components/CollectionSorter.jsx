import React from 'react';

class CollectionSorter extends React.Component {

  constructor(props) {
      super(props);
      this.state = {
        sortOrder: this.props.sortOrder
      }
      this.setSort = this.setSort.bind(this);
  }

  setSort(order) {
    this.setState({sortOrder: order});
    switch(order) {
      case 'AZ':
        this.props.sortAZ();
        break;
      case 'ZA':
        this.props.sortZA();
        break;
      case 'NEW':
        this.props.sortNew();
        break;
      case 'OLD':
        this.props.sortOld();
        break;
      default:
        this.props.sortAZ();
    }
  }

  render() {

    return (
      <div className='sort-component mdc-menu-surface--anchor'>
          <ul className='mdc-list'>
            <li className={this.state.sortOrder === 'AZ' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
               onClick={() => this.setSort("AZ")}>
               <span className='mdc-list-item__text'>A to Z</span>
            </li>
            <li className={this.state.sortOrder === 'ZA' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
               onClick={() => this.setSort("ZA")}>
               <span className='mdc-list-item__text'>Z to A</span>
            </li>
            <li className={this.state.sortOrder === 'NEW' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
               onClick={() => this.setSort("NEW")}>
               <span className='mdc-list-item__text'>Newest</span>
            </li>
            <li className={this.state.sortOrder === 'OLD' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
               onClick={() => this.setSort("OLD")}>
               <span className='mdc-list-item__text'>Oldest</span>
            </li>
          </ul>
      </div>
    )
  }
}

export default CollectionSorter
