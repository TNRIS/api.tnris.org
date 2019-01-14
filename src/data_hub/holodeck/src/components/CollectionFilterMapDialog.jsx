import React from 'react';
import { MDCDialog } from '@material/dialog';

import loadingImage from '../images/loading.gif';

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
        return <CollectionFilterMapContainer history={this.props.history} />
      }
      else {
        return (
          <div className="catalog-component__loading">
            <img src={loadingImage} alt="Holodeck Loading..." className="holodeck-loading-image" />
          </div>
        )
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
                  <div className="instruction-header mdc-typography--body1">
                    <p>
                      Use the 'Polygon tool' in the top left corner  of the map to identify a geographic area for which to filter datasets.
                    </p>
                    <p id="bottom-instruction">
                      Single click to begin drawing, move cursor to draw box of filter extent, single click to finish drawing.
                    </p>
                  </div>
                </header>
                <section className='mdc-dialog__body'>
                  {this.dialogContent()}
                </section>
              </div>
              <button
                className="mdc-fab app-fab--absolute"
                aria-label="Close"
                onClick={this.closeCollectionFilterMapDialog}>
                <span className="mdc-fab__icon material-icons">close</span>
              </button>
              <div className="mdc-dialog__backdrop"></div>
          </aside>
      );
    }
}
