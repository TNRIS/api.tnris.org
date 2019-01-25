import { connect } from 'react-redux';

import CollectionFilterMapView from '../components/CollectionFilterMapView';
import { getAllCollections } from '../selectors/collectionSelectors';

const mapStateToProps = state => ({
  collections: getAllCollections(state)
});

const mapDispatchToProps = dispatch => ({
})

const CollectionFilterMapViewContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CollectionFilterMapView);

export default CollectionFilterMapViewContainer;
