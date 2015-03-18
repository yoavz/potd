// our very own namespace
POTD = {}
POTD.ChartJSType = {
  PIE: 0,
  BAR: 1,
}

// responsive by default
Chart.defaults.global.responsive = true;

function genChart(dataFile, domSelector, type) {
  $.getJSON(dataFile, function (json) {
    // create the graph 
    var ctx = $(domSelector).children("canvas").get(0).getContext("2d");
    switch(type) {
      case POTD.ChartJSType.PIE:
        var cheeseOverall = new Chart(ctx).Pie(json);
        break;
      case POTD.ChartJSType.BAR: 
        var cheeseOverall = new Chart(ctx).Bar(json);
        break;
      default:
        console.log("Invalid chart js type");
    }

    // add the legend
    $(domSelector).children(".legend").html(cheeseOverall.generateLegend());
  });

}

genPieChart = function (f, d) { genChart(f, d, POTD.ChartJSType.PIE); }
genBarChart = function (f, d) { genChart(f, d, POTD.ChartJSType.BAR); }

genPieChart("charts/cheese_overall.json", "#cheese-overall");
genBarChart("charts/cheese_by_month.json", "#cheese-by-month");
