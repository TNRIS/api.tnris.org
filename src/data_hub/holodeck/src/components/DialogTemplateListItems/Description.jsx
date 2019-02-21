import React from 'react';


export default class Description extends React.Component {

  constructor(props) {
    super(props)

    this.state = {
      wikiExtract: ''
    }
  }

  componentDidMount() {
    /////////////////////
    // wiki api stuff
    // if template is outside entity, assign source_name prop to variable
    const wikiName = this.props.collection.template === 'outside-entity' ? this.props.collection.source_name : '';
    // Unauthenticated CORS requests may be made from any origin by setting the "origin" request parameter to "*"
    const wikiUrl = `https://en.wikipedia.org/w/api.php?&origin=*&action=query&prop=extracts&format=json&redirects=1&exintro=&titles=${wikiName}`;
    // reasign this to self so state isn't confused with promise in fetch
    const self = this;

    if (wikiName !== '') {
      fetch(wikiUrl).then(function(response) {
        if (!response.ok) {
          throw new Error('Could not retrieve Wikipedia response.');
        }
        return response.json();
      })
      .then(function(data) {
        const wikiExtract = data.query.pages[Object.keys(data.query.pages)[0]].extract;
        self.setState({wikiExtract:wikiExtract});
      })
    }
    // end wiki api stuff
    /////////////////////
  }

  render() {

    const createMarkup = () => {
      return {__html: this.state.wikiExtract};
    }

    return (
      <div className="template-content-div">
        {
          <div dangerouslySetInnerHTML={createMarkup()} />
        }
        <p>
          {this.props.collection.description}
        </p>
      </div>
    )
  }
}
