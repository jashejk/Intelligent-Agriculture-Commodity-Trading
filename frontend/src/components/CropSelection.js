import React from 'react';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import axios from 'axios';

class CropSelection extends React.Component {
  state = {
    value: 0,
    crops: ['corn', 'wheat', 'oats', 'sorghum']
  }

  handleChange = async (event, newValue) => {
    const crop = this.state.crops[newValue];
    const response = await axios.get(`${window.location.protocol}//${window.location.hostname}:8080/api/crops/?crop=${crop}`);
    this.props.onSelectCrop(crop, response.data.dashboardID, response.data.newsArticles, response.data.market);
    this.setState({ value: newValue });
  }

  render() {
    return (
      <Tabs
        value={this.state.value}
        indicatorColor="primary"
        textColor="primary"
        onChange={this.handleChange}
      >
        {this.state.crops.map((crop, index) => (
          <Tab label={crop} key={index} />
        ))}
      </Tabs>
    );
  }
}

export default CropSelection;
