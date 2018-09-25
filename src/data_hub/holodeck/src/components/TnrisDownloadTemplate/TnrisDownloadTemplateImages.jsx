import React from 'react';

import { Carousel } from 'react-responsive-carousel';

export default class TnrisDownloadTemplateImages extends React.Component {
  constructor(props) {
      super(props);
      console.log(this.props);
  }

  render() {

    // let renderedImages =
    //   this.props.forEach(function () {
    //     if (this.props.natural) {
    //       return (<div><img src={this.props.natural} alt='natural' /></div>);
    //     }
    //     if (this.props.overview) {
    //       return (<div><img src={this.props.overview} alt='overview' /></div>);
    //     }
    //     if (this.props.urban) {
    //       return (<div><img src={this.props.urban} alt='urban' /></div>);
    //     }
    //     else {
    //       return (<div><h3>No images available.</h3></div>);
    //     }
    //   })

    return (

      <div className="tnris-download-template-images">

        <Carousel>

          { if (this.props.natural) {
            return <div><img src={this.props.natural} alt='natural' /></div>
          }

          // <div><img src={this.props.overview} alt='overview' /></div>
          //
          // <div><img src={this.props.urban} alt='urban' /></div>

        </Carousel>

      </div>

    );
  }

}
