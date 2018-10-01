import React from 'react';

import { Carousel } from 'react-responsive-carousel';

export default class TnrisDownloadTemplateImages extends React.Component {
  constructor(props) {
      super(props);
      console.log(this.props);
  }

  render() {

    const imageUrls = [];
    Object.keys(this.props).map(key => this.props[key] !== null ? imageUrls.push(this.props[key]) : '')
    console.log(imageUrls);

    return (

      <div className="tnris-download-template-images">
        <Carousel
          autoPlay={true}
          infiniteLoop={true}
          emulateTouch
          useKeyboardArrows={true}
          transitionTime={1000}
        >
          {
            imageUrls.map(url =>
              <div key={url}>
                <img src={url} alt='' />
              </div>
            )
          }
        </Carousel>
      </div>
    )
  }
}
