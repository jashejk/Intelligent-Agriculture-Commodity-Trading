import React from 'react';

class Dashboard extends React.Component {
  render() {
    const url = `http://public.tableau.com/views/RegionalSampleWorkbook/Storms`;
    return (
      <iframe src={url} width="100%" height="800" frameborder="0"></iframe>
    );
  }
}

export default Dashboard;
