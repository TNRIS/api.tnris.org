import React from 'react';

export default class CollectionFilterMapInstructions extends React.Component {
  constructor(props) {
      super(props);
      this.state = {
        noteHover: false
      };
      this.toggleInstructions = this.toggleInstructions.bind(this);
  }

  toggleInstructions () {
    this.setState({
      noteHover: !this.state.noteHover
    });
  }

  render() {
    const noteContent = this.state.noteHover ? (
      <div>
        <i className="material-icons close-icon" onClick={() => {this.setState({noteHover:false})}}>close</i>
        <div className="mdc-typography--body1 instruction-paragraph">
          Use the 'polygon tool' &nbsp;
          <div id="instruction-polygon-icon" className="mapbox-gl-draw_polygon"></div>&nbsp;
          in the top left corner of the map to identify a geographic area.
        </div>
        <div className="mdc-typography--body1 instruction-paragraph">
          Single click to begin drawing, move cursor to draw a filter extent, single click to finish drawing.
        </div>
      </div>
    ) : (
      <div className="mdc-typography--body1">Instructions</div>
    );

    return (
      <div id='collection-filter-map-instructions'
           className='mdc-typography--caption'
           onClick={() => {this.toggleInstructions()}}>
        {noteContent}
      </div>
    );
  }
}
