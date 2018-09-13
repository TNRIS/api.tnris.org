import React from 'react';
import { MDCDialog } from '@material/dialog';

import TnrisDownloadTemplate from './TnrisDownloadTemplate';
import TnrisOrderTemplate from './TnrisOrderTemplate';
import HistoricalAerialTemplate from './HistoricalAerialTemplate';
import OutsideEntityTemplate from './OutsideEntityTemplate';

class CollectionDialog extends React.Component {
    constructor(props) {
        super(props);
        this.closeCollectionDialog = this.closeCollectionDialog.bind(this);
        this.collectionDialogContent = this.collectionDialogContent.bind(this);
    }

    componentDidMount() {
      this.dialog = new MDCDialog(this.refs.collection_dialog);
    }

    componentDidUpdate() {
      this.props.showCollectionDialog ? this.dialog.show() : this.dialog.close()

    }

    componentWillReceiveProps() {
      this.dialog.listen('MDCDialog:cancel', () => {
        this.closeCollectionDialog();
      })
    }

    collectionDialogContent() {
      if (this.props.showCollectionDialog) {
        let collection = this.props.collections[this.props.selectedCollection];
        switch(collection.template) {
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
    }

    render() {
      return (
        <aside
          ref="collection_dialog"
          id="collection_dialog"
          className="mdc-dialog"
          role="alertdialog"
          aria-labelledby="test_dialog-label"
          aria-describedby="test_dialog-description">
          <div className="mdc-dialog__surface">
            {this.collectionDialogContent()}
              <footer className="mdc-dialog__footer">
                  <button className="mdc-button mdc-button--raised" onClick={this.closeCollectionDialog}>CLOSE</button>
              </footer>
          </div>
          <div className="mdc-dialog__backdrop"></div>
        </aside>
      );
    }
}

export default CollectionDialog;
