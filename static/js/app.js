/* data route */


function buildPlot() {
  


/*
    var trace1 = {
      type: 'scatter',
      mode: 'lines',
      name: 'Bigfoot Sightings',
      x: response.years,
      y: response.sightings,
      line: {
        color: '#17BECF',
      },
    };

    var data = [trace1];

    var layout = {
      title: 'Bigfoot Sightings Per Year',
      xaxis: {
        type: 'date',
      },
      yaxis: {
        autorange: true,
        type: 'linear',
      },
    };

    Plotly.newPlot('plot', data, layout);
    */

}

function dropdown(){
  var url = '/names';
  Plotly.d3.json(url, function(error, response) {
    var dropdown = document.getElementById("selDataset");
    for(i = 0; i<response.length; i++){
      var option = document.createElement('option');
      option.text = option.value = response[i];
      dropdown.add(option);

    }
  });
}
function optionChanged(value){
  var url = '/metadata/'+value;
  var descriptions=[];
  Plotly.d3.json('/otu', function(error, response) {
    console.log(response);
    descriptions=response;
  });
  console.log(descriptions);

  Plotly.d3.json(url, function(error, response) {
    var age = document.getElementById("age");
    var bbtype = document.getElementById("bbtype");
    var ethnicity = document.getElementById("ethnicity");
    var gender = document.getElementById("gender");
    var location = document.getElementById("location");
    var sampleid = document.getElementById("sampleid");
    age.innerHTML="AGE: " + response.AGE;
    bbtype.innerHTML="BBTYPE: " + response.BBTYPE;
    ethnicity.innerHTML="ETHNICITY: " + response.ETHNICITY;
    gender.innerHTML="GENDER: " + response.GENDER;
    location.innerHTML="LOCATION: " + response.LOCATION;
    sampleid.innerHTML="SAMPLEID: " + response.SAMPLEID;
  }); 
  Plotly.d3.json("/samples/"+value, function(error, response) {
    var data = [{
      values: response[0]["sample_values"].slice(0, 10),
      labels: response[0]["otu_ids"].slice(0, 10),
      type:"pie"
    }];
    var layout = {
      height: 600,
      width: 700
    };

    var trace = data[0]

    trace.text = trace.labels.map(function(otu_ids){
      console.log(otu_ids);
      return descriptions [parseInt(otu_ids)];
    });

    trace.hoverinfo="text";

    Plotly.newPlot("piechart", data, layout);
  });

  Plotly.d3.json("/samples/"+value, function(error, response) {
    var trace1 = {
      x: response[0]["otu_ids"],
      y: response[0]["sample_values"],
      text: descriptions,
      mode: 'markers',
      marker: {
        color: response[0]["otu_ids"],
        size: response[0]["sample_values"]
      }
    };
    
    var data = [trace1];
    
    var layout = {
      title: '',
      showlegend: false,
      height: 600,
      width: 1500
    };
    
    Plotly.newPlot('bubblechart', data, layout);
  });

  
}

dropdown();
buildPlot();
