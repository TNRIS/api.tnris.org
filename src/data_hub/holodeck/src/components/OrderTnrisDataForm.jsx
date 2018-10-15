import React, { Component } from 'react';
import {MDCTextField} from '@material/textfield';
import {MDCFloatingLabel} from '@material/floating-label';
import {MDCLineRipple} from '@material/line-ripple';
import {MDCRipple} from '@material/ripple';
import {MDCSelect} from '@material/select';

class OrderTnrisDataForm extends Component {

  constructor(props) {
      super(props);
      console.log(this.props);
      const startDisplay = this.props.orders.hasOwnProperty(this.props.selectedCollection) ? 'cart' : 'form';
      this.state = {
        orderType: '',
        portionDescription: '',
        aoiUpload: '',
        screenshotUpload: '',
        textDescription: '',
        display: startDisplay
      }
      this.collection = this.props.collections[this.props.selectedCollection];
      this.submitForm = this.submitForm.bind(this);
      this.handleChange = this.handleChange.bind(this);
  }

  componentDidMount() {
    document.querySelectorAll('.mdc-floating-label').forEach((mdl) => {
      new MDCFloatingLabel(mdl);
    });
    document.querySelectorAll('.mdc-line-ripple').forEach((mlr) => {
      new MDCLineRipple(mlr);
    });
    document.querySelectorAll('.mdc-text-field').forEach((mtf) => {
      new MDCTextField(mtf);
    });
    document.querySelectorAll('.mdc-button').forEach((mb) => {
      new MDCRipple(mb);
    });
    // new MDCSelect(document.querySelector('.mdc-select'));
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.orders.hasOwnProperty(nextProps.selectedCollection)) {
      this.setState({
        display: 'added'
      });
    }
  }

  componentDidUpdate () {
    console.log(this.state);
    if (this.state.orderType === 'Partial') {
      document.getElementsByName("portionDescription").forEach((input) => {
        input.required = true;
      });
    }
    else {
      document.getElementsByName("portionDescription").forEach((input) => {
        input.required = false;
        input.checked = false;
      });
    }

    if (this.state.portionDescription === 'Text Description') {
      document.getElementsByName("textDescription").forEach((textarea) => {
        textarea.required = true;
      });
    }
    else {
      document.getElementsByName("textDescription").forEach((textarea) => {
        textarea.required = false;
      });
    }
  }

  handleChange(event) {
    const name = event.target.name
    const value = event.target.value
    const nextState = {};
    nextState[name] = value;
    if (name === 'orderType' && value === 'Full') {
      nextState['portionDescription'] = "";
    }
    if (name === 'orderType' && value === 'Full') {
      nextState['portionDescription'] = "";
    }
    this.setState(nextState);
  }

  submitForm (event) {
    event.preventDefault();
    this.props.addCollectionToCart(this.props.selectedCollection, this.props.collections[this.props.selectedCollection]);
    // if (this.state.recaptcha !== '') {
    //   this.setState({
    //     display: 'submitting'
    //   });
    //   console.log('submitting');
    //   const fullName = this.state.firstName + " " + this.state.lastName;
    //
    //   const formInfo = {
    //     'Name': fullName,
    //     'Email': this.state.email,
    //     'Collection': this.props.collection.name,
    //     'Category': this.props.collection.category,
    //     'Software': this.state.software,
    //     'Message': this.state.question,
    //     'form_id': 'data-tnris-org-inquiry',
    //     'recaptcha': this.state.recaptcha
    //   };
    //
    //   console.log(formInfo);
    //   this.props.submitContactTnrisForm(formInfo);
    // }

  }

  render() {
    const partialClass = this.state.orderType === 'Partial' ? "partial-description-field" : "hidden-field";
    const uploadAoiClass = this.state.portionDescription === 'AOI' ? "file-upload-field" : "hidden-field";
    const uploadScreenshotClass = this.state.portionDescription === 'Screenshot' ? "file-upload-field" : "hidden-field";
    const textDescriptionClass = this.state.portionDescription === 'Text Description' ? "text-description-field" : "hidden-field";
    let showHTML;
    let formFields;
    if (this.collection.category === 'Lidar') {
      formFields = (
        <div>

        </div>
      )
    }


    if (this.state.display === 'form') {
      showHTML = (
        <div>
          <p className="mdc-typography--body2">
            Everything you're looking for too large to download? Every dataset is available for order directly from TNRIS.
          </p>

          <div className='mdc-typography--headline6'>
            Dataset Order Type*
          </div>
          <div id="order-type-full" className="mdc-form-field">
            <div className="mdc-radio">
              <input className="mdc-radio__native-control"
                     type="radio"
                     id="order-type-full-input"
                     name="orderType"
                     value="Full"
                     onChange={this.handleChange}
                     required />
              <div className="mdc-radio__background">
                <div className="mdc-radio__outer-circle"></div>
                <div className="mdc-radio__inner-circle"></div>
              </div>
            </div>
            <label htmlFor="order-type-full-input">Full (Entire Dataset)</label>
          </div>
          <div id="order-type-partial" className="mdc-form-field">
            <div className="mdc-radio">
              <input className="mdc-radio__native-control"
                     type="radio"
                     id="order-type-partial-input"
                     name="orderType"
                     value="Partial"
                     onChange={this.handleChange} />
              <div className="mdc-radio__background">
                <div className="mdc-radio__outer-circle"></div>
                <div className="mdc-radio__inner-circle"></div>
              </div>
            </div>
            <label htmlFor="order-type-partial-input">Partial (Described Portion)</label>
          </div>

          <div className={partialClass}>
            <div className='mdc-typography--headline6'>
              Portion Description*
            </div>
            <p className="mdc-typography--body2">
              How would you like to help us identify which portion of the data you need?
            </p>
            <div id="order-partial-aoi" className="mdc-form-field">
              <div className="mdc-radio">
                <input className="mdc-radio__native-control"
                       type="radio"
                       id="order-partial-aoi-input"
                       name="portionDescription"
                       value="AOI"
                       onChange={this.handleChange}
                       required />
                <div className="mdc-radio__background">
                  <div className="mdc-radio__outer-circle"></div>
                  <div className="mdc-radio__inner-circle"></div>
                </div>
              </div>
              <label htmlFor="order-partial-aoi-input">Area of Interest Boundary File (TNRIS Preferred Option)</label>
            </div>
            <div className='mdc-typography--caption'>Select a zipped (.zip) Shapefile or KML to upload. Maximum allowed file size is 20 MB.</div>
            <div className={uploadAoiClass}>
              <input type="file"
                     id="order-partial-aoi-file"
                     name="aoiUpload"
                     accept=".zip,application/octet-stream,application/zip,application/x-zip,application/x-zip-compressed"
                     onChange={this.handleChange}
              />
            </div>
            <div id="order-partial-screenshot" className="mdc-form-field">
              <div className="mdc-radio">
                <input className="mdc-radio__native-control"
                       type="radio"
                       id="order-partial-screenshot-input"
                       name="portionDescription"
                       value="Screenshot"
                       onChange={this.handleChange} />
                <div className="mdc-radio__background">
                  <div className="mdc-radio__outer-circle"></div>
                  <div className="mdc-radio__inner-circle"></div>
                </div>
              </div>
              <label htmlFor="order-partial-screenshot-input">Screenshot with Text Description</label>
            </div>
            <div className='mdc-typography--caption'>Select a .png, .jpg, or .jpeg image to upload. Multiple images are accepted. Maximum allowed file size is 20 MB.</div>
            <div className={uploadScreenshotClass}>
              <input type="file"
                     id="order-partial-screenshot-file"
                     name="screenshotUpload"
                     accept=".png, .jpg, .jpeg"
                     onChange={this.handleChange}
                     multiple />
            </div>
            <div id="order-partial-text" className="mdc-form-field">
              <div className="mdc-radio">
                <input className="mdc-radio__native-control"
                       type="radio"
                       id="order-partial-text-input"
                       name="portionDescription"
                       value="Text Description"
                       onChange={this.handleChange} />
                <div className="mdc-radio__background">
                  <div className="mdc-radio__outer-circle"></div>
                  <div className="mdc-radio__inner-circle"></div>
                </div>
              </div>
              <label htmlFor="order-partial-text-input">Text Description</label>
            </div>
            <div className={textDescriptionClass}>
              <div className='mdc-typography--caption'>Please describe the portion of data you need in the text box below. The more detail provided will vastly improve the response and turn around time of your order.</div>
              <div id="order-partial-text-description" className="mdc-text-field mdc-text-field--textarea">
                <textarea id="order-partial-text-description-input" className="mdc-text-field__input"
                          rows="8" cols="40"
                          placeholder="Latitude/Longitude Coordinates, USGS Quadrangle Names, City/Town Names, Cross Roads, Boundary Landmarks, etc."
                          name="textDescription"
                          onChange={this.handleChange}
                          required>
                </textarea>
                <label className="mdc-floating-label" htmlFor="order-partial-text-description-input">Please describe the portion of data you need...</label>
                <div className="mdc-line-ripple"></div>
              </div>
            </div>
          </div>

          {formFields}

          <div className="submit-button">
            <input type="submit" value="Add to Shopping Cart" id="order-tnris-data-submit" className="mdc-button mdc-button--raised"/>
          </div>
        </div>
      );
    }
    else if (this.state.display === 'cart') {
      showHTML = (
        <div className="order-tnris-data-cart">
          <p className="mdc-typography--body2">
            This dataset is already in your shopping cart.
          </p>
          <p className="mdc-typography--body2">
            Please visit your shopping cart to finalize your order.
          </p>
        </div>
      );
    }
    else if (this.state.display === 'added') {
      showHTML = (
        <div className="order-tnris-data-cart">
          <p className="mdc-typography--body2">
            This dataset has been added to your shopping cart.
          </p>
          <p className="mdc-typography--body2">
            Please visit your shopping cart to finalize your order.
          </p>
        </div>
      );
    }

    return (
      <form className="order-tnris-data-form-component" onSubmit={ this.submitForm }>
        {showHTML}
      </form>
    )
  }
}

export default OrderTnrisDataForm
