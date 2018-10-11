import React from 'react';
import { MDCDialog } from '@material/dialog';
import OrderCartContainer from '../containers/OrderCartContainer';

class OrderCartDialog extends React.Component {
    constructor(props) {
        super(props);
        this.OrderCartDialogContent = this.OrderCartDialogContent.bind(this);
        this.closeOrderCartDialog = this.closeOrderCartDialog.bind(this);
    }

    componentDidMount() {
      this.dialog = new MDCDialog(this.refs.order_cart_dialog);
    }

    componentDidUpdate() {
      this.props.showOrderCartDialog ? this.dialog.show() : this.dialog.close()
    }

    componentWillReceiveProps() {
      this.dialog.listen('MDCDialog:cancel', () => {
        this.closeOrderCartDialog();
      })
    }

    OrderCartDialogContent() {
      return <OrderCartContainer />;
    }

    closeOrderCartDialog() {
      this.props.closeOrderCartDialog();
    }

    render() {
      return (
        <aside
          ref="order_cart_dialog"
          id="order_cart_dialog"
          className="mdc-dialog"
          role="alertdialog"
          aria-labelledby="order_cart_dialog-label"
          aria-describedby="order_cart_dialog-description">
          <div className="mdc-dialog__surface">
            {this.OrderCartDialogContent()}
          </div>
          <button className="mdc-fab app-fab--absolute" aria-label="Close" onClick={this.closeOrderCartDialog}>
            <span className="mdc-fab__icon material-icons">close</span>
          </button>
          <div className="mdc-dialog__backdrop"></div>
        </aside>
      );
    }
}

export default OrderCartDialog;
