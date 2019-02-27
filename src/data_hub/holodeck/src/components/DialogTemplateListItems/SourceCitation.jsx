import React from 'react';

export default class SourceCitation extends React.Component {
  constructor(props) {
    super(props);
    window.innerWidth >= 1000 ? this.state = {
      gridLayout:'desktop',
      copied: false
    } : this.state = {
      gridLayout:'mobile',
      copied: false
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
    document.getElementById("citation").select();
    document.execCommand("copy");
    this.setState({copied: true});
  }

  render() {

    const copied = this.state.copied ? "Copied!" : "Copy";
    const currentDate = new Date();
    const sourceCitationText = `${this.props.collection.source_name} (${this.props.collection.source_abbreviation}). ${this.props.collection.name}, ${this.props.collection.acquisition_date}. Web. ${currentDate}`
    const textAreaRows = this.state.gridLayout === 'desktop' ? "8" : "2";
    const textAreaCols = this.state.gridLayout === 'desktop' ? "20" : "10";

    return (
      <div className="template-content-div">
        <div className="citation-container">
          <div className="mdc-typography--headline5">
            Source Citation
          </div>
          <div className="citation-style">
            Copy the text below to cite this dataset.
          </div>
          <textarea id="citation"
            className="mdc-text-field__input copy-citation"
            rows={textAreaRows}
            columns={textAreaCols}
            value={sourceCitationText}
            readOnly>
          </textarea>
          <div className="services-link-details">
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
