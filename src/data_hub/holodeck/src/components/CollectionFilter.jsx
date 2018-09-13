import React from 'react';

export default class CollectionFilter extends React.Component {
  constructor(props) {
    super(props);
    this.handleSetFilter = this.handleSetFilter.bind(this);
  }

  handleSetFilter() {
    this.props.setCollectionFilter({
      category: 'Environmental',
      recommended_use: 'General Large Scale Geologic Information and Mapping'
    });
  }

  render() {
    console.log(this.props);
    return (
      <div>
        <button onClick={this.handleSetFilter}>filter</button>
      </div>
    );
  }
}
