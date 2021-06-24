$.get('/comparison.json', (res) => {
    const data = [];
    for (const type of res.data) {
      data.push({x: type.type, y: type.ratio});
    }
  
    new Chart(
      $('#comparison-chart'),
      {
        type: 'bar',
        data: {
          datasets: [
            {
              label: 'Similarity Comparison',
              data: data
            }
          ]
        }
      }
    );
  });