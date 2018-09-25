import React from 'react';

import { Carousel } from 'react-responsive-carousel';

export default class TnrisDownloadTemplateImages extends React.Component {
  constructor(props) {
      super(props);
      console.log(this.props);
      this.renderImages = this.renderImages.bind(this);
  }

  renderImages() {
    Object.keys(this.props).map(key => {
      console.log(key);
      if (this.props[key]) {
        console.log(key);
        let imageDiv =
          <div>
            <img src={this.props[key]} alt='Image' />
          </div>
        ;
      }
    })
  }

  render() {

    // const propArray = Object.keys(this.props);
    // console.log(propArray);
    // console.log(this.props);
    const imageUrls = [];
    Object.keys(this.props).map(key => this.props[key] !== null ? imageUrls.push(this.props[key]) : '')
    console.log(imageUrls);

    return (

      <div className="tnris-download-template-images">
        <Carousel>
          {
            imageUrls.map(url =>
              <div key={url}>
                <img src={url} alt='Image' />
              </div>
            )
          }
        </Carousel>
      </div>

    )


    // for (var i in propArray) {
    //   console.log(propArray.map);
    //
    //   console.log(this.props[propArray[i]]);
    //
    //   if (this.props[propArray[i]] !== null) {
    //     return (
    //       <div className="tnris-download-template-images">
    //         <Carousel>
    //           <div>
    //             <img src={this.props[propArray[i]]} alt='Image' />
    //           </div>
    //         </Carousel>
    //       </div>
    //     );
    //   } else {
    //     return (
    //       <div className="tnris-download-template-images">
    //         <Carousel>
    //           <div>
    //             <h1></h1>
    //           </div>
    //         </Carousel>
    //       </div>
    //     )
    //   };

        // <div className="tnris-download-template-images">
        //   <Carousel>
        //     <div>
        //       <img src={this.props[propArray[i]]} alt='Image' />
        //     </div>
        //   </Carousel>
        // </div>


    }
  }
