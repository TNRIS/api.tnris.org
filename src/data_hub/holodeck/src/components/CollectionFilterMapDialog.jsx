import React from 'react';
import { MDCDialog } from '@material/dialog';

import CollectionFilterMap from './CollectionFilterMap';

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
      return <CollectionFilterMap />
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
              aria-labelledby="map_dialog-label"
              aria-describedby="map_dialog-description">
              <div className="mdc-dialog__surface">
                <header className='mdc-dialog__header'>
                  <h2 className='mdc-dialog__header__title'>
                    map
                  </h2>
                </header>
                <section className='mdc-dialog__body'>
                  {this.dialogContent()}
                </section>
                <footer className="mdc-dialog__footer">
                    <button onClick={this.closeCollectionFilterMapDialog}>CLOSE</button>
                </footer>
              </div>
              <div className="mdc-dialog__backdrop"></div>
          </aside>
      );
    }
}
