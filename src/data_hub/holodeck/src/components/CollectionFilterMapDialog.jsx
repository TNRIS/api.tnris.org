import React from 'react';
import { MDCDialog } from '@material/dialog';

import CollectionFilterMapContainer from '../containers/CollectionFilterMapContainer';

export default class CollectionFilterMapDialog extends React.Component {
    constructor(props) {
        super(props);
        this.dialogContent = this.dialogContent.bind(this);
        this.closeCollectionFilterMapDialog = this.closeCollectionFilterMapDialog.bind(this);
    }

    componentDidMount() {
      this.dialog = new MDCDialog(this.refs.filter_map_dialog);
    }

    componentDidUpdate() {
      this.props.showCollectionFilterMapDialog ? this.dialog.show() : this.dialog.close()

    }

    componentWillReceiveProps() {
      this.dialog.listen('MDCDialog:cancel', () => {
        this.closeCollectionFilterMapDialog();
      })
    }

    dialogContent() {
      if (this.props.showCollectionFilterMapDialog) {
        return <CollectionFilterMapContainer />
      }
    }

    closeCollectionFilterMapDialog() {
      this.props.closeCollectionFilterMapDialog();
    }

    render() {
      return (
          <aside
              ref="filter_map_dialog"
              id="filter_map_dialog"
              className="mdc-dialog"
              role="alertdialog"
              aria-labelledby="filter_map_dialog-label"
              aria-describedby="filter_map_dialog-description">
              <div className="mdc-dialog__surface">
                <header className='mdc-dialog__header'>
                  <h2 className='mdc-dialog__header__title'>
                    filter map
                  </h2>
                </header>
                <section className='mdc-dialog__body'>
                  {this.dialogContent()}
                </section>
                <button
                  className="mdc-fab app-fab--absolute"
                  aria-label="Close"
                  onClick={this.closeCollectionFilterMapDialog}>
                  <span className="mdc-fab__icon material-icons">close</span>
                </button>
              </div>
              <div className="mdc-dialog__backdrop"></div>
          </aside>
      );
    }
}
