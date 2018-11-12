import React from 'react';
import { Redirect } from 'react-router';
import Range from 'rc-slider/lib/Range';

import 'rc-slider/assets/index.css';

export default class CollectionTimeslider extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      range: this.props.collectionTimeslider,
      setMin: this.props.collectionTimeslider[0],
      setMax: this.props.collectionTimeslider[1],
      badUrlFlag: false
    }
    this.handleSetTimeslider = this.handleSetTimeslider.bind(this);
  }

  componentDidMount () {
    if (this.props.collectionTimesliderRange !== this.state.range) {
      this.setState({
        range: this.props.collectionTimesliderRange,
        setMin: this.props.collectionTimesliderRange[0],
        setMax: this.props.collectionTimesliderRange[1]
      });
    }
    // on component mount, check the URl to apply any necessary filters
    // first, check if url has a 'filters' parameter
    if (Object.keys(this.props.match.params).includes('filters')) {
      try {
        const allFilters = JSON.parse(decodeURIComponent(this.props.match.params.filters));
        // second, check if filters param includes range key
        if (Object.keys(allFilters).includes('range')) {
          // third, apply range and set state to reflect it
          this.setState({
            setMin: allFilters.range[0],
            setMax: allFilters.range[1]
          });
          this.props.setCollectionTimeslider(allFilters.range);
        }
      } catch (e) {
        console.log(e);
        this.setState({
          badUrlFlag: true
        });
      }
    }
  }

  handleSetTimeslider(target) {
    this.setState({
      setMin: target[0],
      setMax: target[1]
    });
    this.props.setCollectionTimeslider(target);

    // update URL to reflect new timeslider changes
    const prevFilter = this.props.history.location.pathname.includes('/catalog/') ?
                       JSON.parse(decodeURIComponent(this.props.history.location.pathname.replace('/catalog/', '')))
                       : {};
    const filterObj = {...prevFilter, range: target};
    // if timeslider at full range, remove from the url completely
    if (filterObj['range'][0] === this.state.range[0] && filterObj['range'][1] === this.state.range[1]) {
      delete filterObj['range'];
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
      <div className='timeslider-component'>
        <div className="mdc-typography--body2">{this.state.setMin} - {this.state.setMax}</div>
        <Range min={this.state.range[0]}
               max={this.state.range[1]}
               defaultValue={this.state.range}
               pushable={true}
               onChange={() => this.handleSetTimeslider} />
      </div>
    );
  }
}
