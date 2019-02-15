import { connect } from 'react-redux';

import { catalogActions,
         collectionActions,
         urlTrackerActions } from '../actions';
import CatalogCard from '../components/CatalogCard';

const mapStateToProps = state => ({
  selectedCollection: state.collections.selectedCollection
});

const mapDispatchToProps = (dispatch) => ({
    selectCollection: (collectionId) => {
      dispatch(collectionActions.selectCollection(collectionId));
    },
    setUrl: (newUrl, history) => {
      dispatch(urlTrackerActions.setUrl(newUrl, history))
    },
    setViewCollection: () => {
      dispatch(catalogActions.setViewCollection());
    }
})

const CatalogCardContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CatalogCard);

export default CatalogCardContainer;
