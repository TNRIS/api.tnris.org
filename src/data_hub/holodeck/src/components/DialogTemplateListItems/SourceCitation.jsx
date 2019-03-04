import React from 'react';

export default class SourceCitation extends React.Component {
  constructor(props) {
    super(props);
    window.innerWidth >= 1000 ? this.state = {
      gridLayout:'desktop',
      copied: false,
      date: new Date()
    } : this.state = {
      gridLayout:'mobile',
      copied: false,
      date: new Date()
    };

    this.handleResize = this.handleResize.bind(this);
    this.copySourceCitation = this.copySourceCitation.bind(this);
  }

  componentDidMount() {
    window.addEventListener("resize", this.handleResize);
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this.handleResize);
  }

  handleResize() {
    if (window.innerWidth >= 1000) {
      this.setState({gridLayout:'desktop'});
    }
    else {
      this.setState({gridLayout:'mobile'});
    }
  }

  copySourceCitation () {
    const textarea = document.getElementById("citation");
    textarea.select();
    this.setState({copied: true});
    document.execCommand("copy");
  }

  render() {

    const copied = this.state.copied ? "Copied!" : "Copy";
    const sourceCitationText = `${this.props.collection.source_name} (${this.props.collection.source_abbreviation}). ${this.props.collection.name}, ${this.props.collection.acquisition_date}. Web. ${this.state.date}`
    const textAreaRows = this.state.gridLayout === 'desktop' ? "4" : "2";

    return (
      <div className="template-content-div">
        <div className="citation-container">
          <div className="mdc-typography--subtitle1 citation-header">
            Dataset Citation
          </div>
          <div className="mdc-typography--subtitle2 citation-help">
            Copy the text below to cite this dataset.
          </div>
          <textarea
            type="text"
            id="citation"
            className="mdc-text-field__input citation"
            rows={textAreaRows}
            value={sourceCitationText}
            readOnly>
          </textarea>
          <div className="citation-button-container services-link-details">
            <div className="service-link-details-buttons">
              <button className="mdc-button mdc-button--raised" onClick={this.copySourceCitation}>
                <i className="material-icons">file_copy</i>{copied}
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }
}
