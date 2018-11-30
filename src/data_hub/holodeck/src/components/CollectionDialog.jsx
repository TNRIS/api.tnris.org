import React from 'react';
import { MDCDialog } from '@material/dialog';

import TnrisDownloadTemplate from './TnrisDownloadTemplate/TnrisDownloadTemplate';
import TnrisOrderTemplate from './TnrisOrderTemplate/TnrisOrderTemplate';
import HistoricalAerialTemplate from './HistoricalAerialTemplate/HistoricalAerialTemplate';
import OutsideEntityTemplate from './TnrisOutsideEntityTemplate/TnrisOutsideEntityTemplate';

class CollectionDialog extends React.Component {
    constructor(props) {
        super(props);
        this.closeCollectionDialog = this.closeCollectionDialog.bind(this);
        this.collectionDialogContent = this.collectionDialogContent.bind(this);
    }

    componentDidMount() {
      this.dialog = new MDCDialog(this.refs.collection_dialog);

      // wire cancel event to handle closing the dialog via ESC key or clicking
      // the backdrop. simply running this.closeCollectionDialog() trips up the
      // app so we have to clear the store's selected collection below in the
      // componentWillReceiveProps lifecycle function after the dialog is closed
      this.dialog.listen('MDCDialog:cancel', () => {
        this.props.closeCollectionDialog();
        if (this.props.previousUrl.includes('/collection/')) {
          this.props.setUrl('/', this.props.history);
        }
        else {
          this.props.setUrl(this.props.previousUrl, this.props.history);
        }
      })
    }

    componentWillReceiveProps (nextProps) {
      // must be very specific about the dialog switching from redux declared
      // closed to open and vice versa. firing this.dialog.show() and .close()
      // with every prop update causing material to fire unwanted animations
      if (!this.props.showCollectionDialog && nextProps.showCollectionDialog) {
        this.dialog.show();
      }
      else if (this.props.showCollectionDialog && !nextProps.showCollectionDialog) {
        this.dialog.close();
      }

      if (nextProps.selectedCollection && !nextProps.showCollectionDialog) {
        this.props.clearSelectedCollection();
      }
    }

    collectionDialogContent() {
      if (this.props.showCollectionDialog) {
        let collection = this.props.collections[this.props.selectedCollection];
        switch(collection['template']) {
          case 'tnris-download':
            return (<TnrisDownloadTemplate collection={collection} />);
          case 'tnris-order':
            return (<TnrisOrderTemplate collection={collection} />);
          case 'historical-aerial':
            return (<HistoricalAerialTemplate collection={collection} />);
          case 'outside-entity':
            return (<OutsideEntityTemplate collection={collection} />);
          default:
            return (<TnrisDownloadTemplate collection={collection} />);
        }

      }
    }

    closeCollectionDialog() {
      this.props.closeCollectionDialog();
      this.props.clearSelectedCollection();
      if (this.props.previousUrl.includes('/collection/')) {
        this.props.setUrl('/', this.props.history);
      }
      else {
        this.props.setUrl(this.props.previousUrl, this.props.history);
      }
    }

    render() {
      return (
        <aside
          ref="collection_dialog"
          id="collection_dialog"
          className="mdc-dialog"
          role="alertdialog"
          aria-labelledby="collection_dialog-label"
          aria-describedby="collection_dialog-description">
          <div className="mdc-dialog__surface">
            {this.collectionDialogContent()}
          </div>
          <button className="mdc-fab app-fab--absolute" aria-label="Close" onClick={this.closeCollectionDialog}>
            <span className="mdc-fab__icon material-icons">close</span>
          </button>
          <div className="mdc-dialog__backdrop"></div>
        </aside>
      );
    }
}

export default CollectionDialog;
