import { connect } from 'react-redux';
import { getResourceAreas } from '../selectors/resourceSelectors';
import TnrisDownloadTemplateDownload from '../components/TnrisDownloadTemplate/TnrisDownloadTemplateDownload';

const mapStateToProps = state => ({
  loadingResources: state.collections.loadingResources,
  errorResources: state.collections.errorResources,
  selectedCollectionResources: state.collections.selectedCollectionResources,
  resourceAreas: getResourceAreas(state)
});

const mapDispatchToProps = (dispatch) => ({

})

const TnrisDownloadTemplateDownloadContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(TnrisDownloadTemplateDownload);

export default TnrisDownloadTemplateDownloadContainer;
