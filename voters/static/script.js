function switchVis(value) {
    chartId = value;  // Update the global chartId based on the drop down selection.
    // You can now update your visualization accordingly.
    console.log("Current chartId:", chartId);
    document.querySelector('iframe').src = 'https://datawrapper.dwcdn.net/' + chartId;
  }
