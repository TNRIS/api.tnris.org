import { connect } from 'react-redux';

import OrderCartView from '../components/OrderCartView';

import { catalogActions,
         collectionActions,
         toolDrawerActions,
         urlTrackerActions } from '../actions';

const mapStateToProps = state => ({
  previousUrl: state.urlTracker.previousUrl
});

const mapDispatchToProps = dispatch => ({
  setUrl: (newUrl, history) => {
    dispatch(urlTrackerActions.setUrl(newUrl, history))
  },
  setViewCatalog: () => {
    dispatch(catalogActions.setViewCatalog());
  },
  setViewCollection: () => {
    dispatch(catalogActions.setViewCollection());
  },
  selectCollection: (collectionId) => {
    dispatch(collectionActions.selectCollection(collectionId));
  },
  openToolDrawer: () => {
    dispatch(toolDrawerActions.openToolDrawer());
  },
})

const OrderCartViewContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(OrderCartView);

export default OrderCartViewContainer;
