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
        var chart = new Chart(ctx).Pie(json);
        break;
      case POTD.ChartJSType.BAR: 
        var chart = new Chart(ctx).Bar(json);
        break;
      default:
        console.log("Invalid chart js type");
    }

    // add the legend
    $(domSelector).children(".legend").html(chart.generateLegend());
  });

}

genPieChart = function (f, d) { genChart(f, d, POTD.ChartJSType.PIE); }
genBarChart = function (f, d) { genChart(f, d, POTD.ChartJSType.BAR); }

genPieChart("charts/base_overall.json", "#base-overall");
genBarChart("charts/base_by_month.json", "#base-by-month");
genPieChart("charts/ingredients_overall.json", "#ingredients-overall");
