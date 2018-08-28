import { connect } from 'react-redux';

import { collectionActions, resourceActions } from '../actions';
import Catalog from '../components/Catalog';

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

const CatalogContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Catalog);

export default CatalogContainer;
