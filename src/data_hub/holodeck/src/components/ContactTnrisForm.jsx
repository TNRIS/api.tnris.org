import React, { Component } from 'react';
import {MDCTextField} from '@material/textfield';
import {MDCFloatingLabel} from '@material/floating-label';

class ContactTnrisForm extends Component {

  constructor(props) {
      super(props);
      console.log(this.props);
  }

  componentDidMount() {
    // const textField = new MDCTextField(document.querySelector('.mdc-text-field'));
    const floatingLabel = new MDCFloatingLabel(document.querySelector('.mdc-floating-label'));
  }

  render() {

    return (
      <div className="contact-tnris-form-component">
        <label className="mdc-text-field">
          <input type="text" className="mdc-text-field__input" />
          <span className="mdc-floating-label">Hint text</span>
          <div className="mdc-text-field__bottom-line"></div>
        </label>

      </div>
    )
  }
}

export default ContactTnrisForm
