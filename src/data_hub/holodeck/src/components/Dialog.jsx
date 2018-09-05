import React from 'react';
import { MDCDialog } from '@material/dialog';

import CollectionCard from './CollectionCard';
import Map from './Map';

class Dialog extends React.Component {
    constructor(props) {
        super(props);
        this.dialogContent = this.dialogContent.bind(this);
        this.closeDialog = this.closeDialog.bind(this);
    }

    componentDidMount() {
      console.log(this.props);
      this.dialog = new MDCDialog(this.refs.dialog);
    }

    componentDidUpdate() {
      console.log(this.props);
      this.props.showDialog ? this.dialog.show() : this.dialog.close()

    }

    componentWillReceiveProps() {
      this.dialog.listen('MDCDialog:cancel', () => {
        this.closeDialog();
      })
    }

    dialogContent() {
      return this.props.selectedCollection ?
        <CollectionCard
          collection={this.props.collections.entities.collectionsById[this.props.selectedCollection]}
        /> : <Map />
    }

    closeDialog() {
      this.props.closeDialog();
      this.props.clearSelectedCollection();
    }

    render() {
      return (
          <aside
              ref="dialog"
              id="test_dialog"
              className="mdc-dialog"
              role="alertdialog"
              aria-labelledby="test_dialog-label"
              aria-describedby="test_dialog-description">
              <div className="mdc-dialog__surface">
                {this.dialogContent()}
                  <footer className="mdc-dialog__footer">
                      <button onClick={this.closeDialog}>CLOSE</button>
                  </footer>
              </div>
              <div className="mdc-dialog__backdrop"></div>
          </aside>
      );
    }
}

export default Dialog;
