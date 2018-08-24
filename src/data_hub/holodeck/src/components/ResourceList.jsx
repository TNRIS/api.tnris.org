import React from 'react';
import { connect } from 'react-redux';

import { collectionActions, resourceActions } from '../actions';

class ResourceList extends React.Component {

  componentDidMount() {
    console.log(this.props);
    this.props.fetchCollections();
    this.props.fetchResources();
  }

  render() {
    console.log(this.props);
    const { error, loading, resources } = this.props;

    if (error) {
      return <div>Error! {error.message}</div>;
    }

    if (loading) {
      return <div>Loading...</div>;
    }

    return (
      <div className='container'>
        <div className='row'>
          <h3 className='col text-left'>Resources</h3>
        </div>
        <ul className='list-group'>
          {resources.map((resource, i) =>
            <li className='list-group-item' key={i}><h6>{resource.resource}</h6></li>
          )}
        </ul>
      </div>
    );
  }
}

const mapStateToProps = state => ({
  collections: state.collections.items,
  resources: state.resources.items,
  loading: state.collections.loading,
  error: state.collections.error
});

const mapDispatchToProps = dispatch => ({
  fetchCollections: () => {
    dispatch(collectionActions.fetchCollections());
  },
  fetchResources: () => {
    dispatch(resourceActions.fetchResources());
  }
})

export default connect(mapStateToProps, mapDispatchToProps)(ResourceList);
