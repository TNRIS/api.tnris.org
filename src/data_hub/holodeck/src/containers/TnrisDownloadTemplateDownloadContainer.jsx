import { connect } from 'react-redux';

import TnrisDownloadTemplateDownload from '../components/TnrisDownloadTemplate/TnrisDownloadTemplateDownload';

const mapStateToProps = state => ({
  loadingResources: state.collections.loadingResources,
  errorResources: state.collections.errorResources,
  selectedCollectionResources: state.collections.selectedCollectionResources
});

const mapDispatchToProps = (dispatch) => ({

})

const TnrisDownloadTemplateDownloadContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(TnrisDownloadTemplateDownload);

export default TnrisDownloadTemplateDownloadContainer;
