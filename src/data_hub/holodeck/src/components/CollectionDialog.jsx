import React from 'react';
import { MDCDialog } from '@material/dialog';

class CollectionDialog extends React.Component {
    constructor(props) {
        super(props);
        this.closeCollectionDialog = this.closeCollectionDialog.bind(this);
        this.collectionDialogContent = this.collectionDialogContent.bind(this);
    }

    componentDidMount() {
      console.log(this.props);
      this.dialog = new MDCDialog(this.refs.collection_dialog);
    }

    componentDidUpdate() {
      console.log(this.props);
      this.props.showCollectionDialog ? this.dialog.show() : this.dialog.close()

    }

    componentWillReceiveProps() {
      this.dialog.listen('MDCDialog:cancel', () => {
        this.closeCollectionDialog();
      })
    }

    collectionDialogContent() {
      if (this.props.showCollectionDialog) {
        let collection = this.props.collections.entities.collectionsById[this.props.selectedCollection];
        return (
          <div className='collection-dialog mdc-layout-grid'>
            <div className='mdc-layout-grid__inner'>
              <h4 className='mdc-typography--headline4 mdc-layout-grid__cell mdc-layout-grid__cell--span-12'>
                {collection.name}
              </h4>
            </div>
              <img src={collection.overview_image} alt=''
                    className='collection-dialog__image mdc-layout-grid__cell--span-12'/>
            <div className='mdc-layout-grid__inner'>
              <p className='mdc-typography__body2 mdc-layout-grid__cell--span-12'>
                {collection.description}
              </p>
            </div>
          </div>
        )
      }
    }

    closeCollectionDialog() {
      this.props.closeCollectionDialog();
      this.props.clearSelectedCollection();
    }

    render() {
      console.log(this.props);
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
                  <button onClick={this.closeCollectionDialog}>CLOSE</button>
              </footer>
          </div>
          <div className="mdc-dialog__backdrop"></div>
        </aside>
      );
    }
}

export default CollectionDialog;
