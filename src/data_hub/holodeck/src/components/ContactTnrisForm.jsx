import React, { Component } from 'react';
import {MDCTextField} from '@material/textfield';
import {MDCFloatingLabel} from '@material/floating-label';
import {MDCLineRipple} from '@material/line-ripple';
import {MDCRipple} from '@material/ripple';
import {MDCSelect} from '@material/select';

class ContactTnrisForm extends Component {

  constructor(props) {
      super(props);
      console.log(this.props);
      this.state = {
        firstName: '',
        lastName: '',
        email: '',
        software: '',
        question: '',
        display: 'form'
      }
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
    new MDCRipple(document.querySelector('#contact-tnris-submit'));
    new MDCSelect(document.querySelector('.mdc-select'));
  }

  componentWillUpdate(nextProps) {
    if (nextProps.submitStatus === false &&
        nextProps.errorStatus !== null &&
        this.state.display === 'submitting') {
      this.setState({
        display: 'error'
      });
    }
    else if (nextProps.submitStatus === false &&
             nextProps.errorStatus === null &&
             this.state.display === 'submitting') {
      this.setState({
       display: 'success'
      });
    }
  }

  handleChange(event) {
    const name = event.target.name
    const value = event.target.value
    const nextState = {};
    nextState[name] = value;
    this.setState(nextState);
  }

  submitForm (event) {
    event.preventDefault()
    this.setState({
      display: 'submitting'
    });
    console.log('submitting');
    const fullName = this.state.firstName + " " + this.state.lastName;

    const formInfo = {
      'Name': fullName,
      'Email': this.state.email,
      'Collection': this.props.collection.name,
      'Category': this.props.collection.category,
      'Software': this.state.software,
      'Message': this.state.question,
      'form_id': 'data-tnris-org-inquiry'
    };

    console.log(formInfo);
    this.props.submitContactTnrisForm(formInfo);

  }

  render() {
    let showHTML;

    if (this.state.display === 'form') {
      showHTML = (
        <div>
          <p>
            Complete the form below to inquire with TNRIS about the <strong>{this.props.collection.name}</strong> dataset...
          </p>

          <div id="ct-first-name" className="mdc-text-field mdc-text-field--outlined">
            <input type="text" id="ct-first-name-input"
                   className="mdc-text-field__input"
                   name="firstName"
                   onChange={this.handleChange}
                   required />
            <label className="mdc-floating-label" htmlFor="ct-first-name-input">First Name</label>
            <div className="mdc-line-ripple"></div>
          </div>

          <div id="ct-last-name" className="mdc-text-field mdc-text-field--outlined">
            <input type="text" id="ct-last-name-input"
                   className="mdc-text-field__input"
                   name="lastName"
                   onChange={this.handleChange}
                   required />
            <label className="mdc-floating-label" htmlFor="ct-last-name-input">Last Name</label>
            <div className="mdc-line-ripple"></div>
          </div>

          <div id="ct-email" className="mdc-text-field mdc-text-field--outlined">
            <input type="email" id="ct-email-input"
                   className="mdc-text-field__input"
                   name="email"
                   onChange={this.handleChange}
                   required />
            <label className="mdc-floating-label" htmlFor="ct-email-input">Email</label>
            <div className="mdc-line-ripple"></div>
          </div>

          <div className="mdc-select">
            <select className="mdc-select__native-control" defaultValue=""
                    name="software"
                    onChange={this.handleChange}
                    required>
              <option value="" disabled>Software Being Used...</option>
              <option value="ArcMap">ArcMap</option>
              <option value="ENVI">ENVI</option>
              <option value="ERDAS">ERDAS</option>
              <option value="Global Mapper">Global Mapper</option>
              <option value="Integraph">Integraph</option>
              <option value="LP360">LP360</option>
              <option value="Microstation">Microstation</option>
              <option value="PostGIS">PostGIS</option>
              <option value="QGIS">QGIS</option>
              <option value="Other">Other</option>
            </select>
            <label className="mdc-floating-label">Software Being Used</label>
            <div className="mdc-line-ripple"></div>
          </div>


          <div id="ct-question" className="mdc-text-field mdc-text-field--textarea">
            <textarea id="ct-question-input" className="mdc-text-field__input"
                      rows="8" cols="40"
                      placeholder="Question or Comment about this dataset..."
                      name="question"
                      onChange={this.handleChange}
                      required>
            </textarea>
            <label className="mdc-floating-label" htmlFor="ct-question-input">Question</label>
            <div className="mdc-line-ripple"></div>
          </div>

          <div>
            <input type="submit" value="Submit" id="contact-tnris-submit" className="mdc-button mdc-button--raised"/>
          </div>
        </div>
      );
    }
    else if (this.state.display === 'success') {
      showHTML = (
        <div className="contact-tnris-form-success">
          <p>
            <span><strong>Success!</strong></span>
            <br />
            Thank you for submitting your inquiry. We review submissions in a timely manner. (unless you are claiming our <strong>"data is corrupt"</strong>; in which case, we will NOT respond because our data is NOT corrupt. you are just a dumb-dumb.)
          </p>
        </div>
      );
    }
    else if (this.state.display === 'error') {
      showHTML = (
        <div className="contact-tnris-form-error">
          <p>
            <span><strong>Error!</strong></span>
            <br />
            Unfortunately, we have encountered an error. Please wait a moment, refresh the page, and try again.
            <br />
            <br />
            {this.props.errorStatus.toString()}
          </p>
        </div>
      );
    }
    else if (this.state.display === 'submitting') {
      showHTML = (
        <div className="contact-tnris-form-submitting">
          <p>
            <span><strong>Submitting form...</strong></span>
          </p>
        </div>
      );
    }

    return (
      <form className="contact-tnris-form-component" onSubmit={ this.submitForm }>
        {showHTML}
      </form>
    )
  }
}

export default ContactTnrisForm
