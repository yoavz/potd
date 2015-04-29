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
    var ctx = $(domSelector).find("canvas").get(0).getContext("2d");
    switch(type) {
      case POTD.ChartJSType.PIE:
        var chart = new Chart(ctx).Pie(json);
        break;
      case POTD.ChartJSType.BAR: 
        var chart = new Chart(ctx).Bar(json);
        break;
      case "scatter":
        var chart = new Chart(ctx).Scatter(json, {
          datasetStroke: false, // no lines
          pointDotStrokeWidth: 0,
          // pointDotRadius: 2,
          // pointHitRadius: 2
        }); 
        break;
      default:
        console.log("Invalid chart js type");
    }

    // add the legend
    $(domSelector).find(".legend-scale").html(chart.generateLegend());
  });

}

genPieChart = function (f, d) { genChart(f, d, POTD.ChartJSType.PIE); }
genBarChart = function (f, d) { genChart(f, d, POTD.ChartJSType.BAR); }
genScatterChart = function (f, d) { genChart(f, d, "scatter"); }

genPieChart("charts/base_overall.json", "#base-overall");
genBarChart("charts/base_by_month.json", "#base-by-month");
genBarChart("charts/base_by_weekday.json", "#base-by-weekday");

genBarChart("charts/ingredients_overall.json", "#toppings-overall");
genBarChart("charts/ingredient_pairings.json", "#topping-pairings");
genBarChart("charts/base_ingredient_pairings.json", "#base-topping-pairings");

genBarChart("charts/base_likes.json", "#base-likes");
genBarChart("charts/ingredients_likes.json", "#ingredients-likes");
genBarChart("charts/likes_by_weekday.json", "#likes-by-weekday");

genScatterChart("charts/likes_by_time.json", "#likes-by-time");
