import React from 'react';


export default class Description extends React.Component {

  render() {

    let wikiName = this.props.collection.template === 'outside-entity' && this.props.collection.source_name.includes(' ') ? this.props.collection.source_name.split(' ').join('_') : '';
    let wikiRequestUrl = wikiName !== '' ? `https://en.wikipedia.org/w/api.php?action=query&origin=*&format=json&generator=search&gsrnamespace=0&gsrlimit=5&gsrsearch='${wikiName}'` : '';

    if (wikiName !== '') {
      fetch(wikiRequestUrl)
        .then(function(response) {
          return response.json();
        })
        .then(function(outsideJson) {
          console.log(JSON.stringify(outsideJson));
        });
    }

    console.log(wikiName);
    console.log(wikiRequestUrl);

    return (
      <div className="template-content-div">
        <p>
          {this.props.collection.description}
        </p>
      </div>
    )
  }
}
