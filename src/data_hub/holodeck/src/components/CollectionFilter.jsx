import React from 'react';

export default class CollectionFilter extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      filter: false
    }
    this.handleSetFilter = this.handleSetFilter.bind(this);
  }

  handleSetFilter() {
    this.setState({filter: !this.state.filter}, () => {
      console.log(this.state);
      if (this.state.filter) {
        console.log('filter');
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
    console.log(this.state);
    return (
      <div>
        <button onClick={this.handleSetFilter}>filter</button>
      </div>
    );
  }
}
