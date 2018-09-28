import React from 'react';
import { MDCDialog } from '@material/dialog';

import Map from './Map';

class MapDialog extends React.Component {
    constructor(props) {
        super(props);
        this.dialogContent = this.dialogContent.bind(this);
        this.closeMapDialog = this.closeMapDialog.bind(this);
    }

    componentDidMount() {
      this.dialog = new MDCDialog(this.refs.map_dialog);
    }

    componentDidUpdate() {
      this.props.showMapDialog ? this.dialog.show() : this.dialog.close()

    }

    componentWillReceiveProps() {
      this.dialog.listen('MDCDialog:cancel', () => {
        this.closeMapDialog();
      })
    }

    dialogContent() {
      return <Map />
    }

    closeMapDialog() {
      this.props.closeMapDialog();
    }

    render() {
      return (
          <aside
              ref="map_dialog"
              id="map_dialog"
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
                    <button onClick={this.closeMapDialog}>CLOSE</button>
                </footer>
              </div>
              <div className="mdc-dialog__backdrop"></div>
          </aside>
      );
    }
}

export default MapDialog;
