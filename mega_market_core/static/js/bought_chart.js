function bought_chart(chart_date_format, filters_to_apply) {
    var current_date = new Date();
    var current_year = current_date.getFullYear();
    var current_month = current_date.getMonth();
    var current_day = current_date.getDate();

    $.ajax({
        method: "GET",
        url: 'http://127.0.0.1:8000/api/bought/',
        data: filters_to_apply,
        success: function (data) {

            console.log(data)
            var Bought_report = data.bought_report_chart

            var graph_data = [
                {"stat": 'data_sum', "value": Bought_report.data_sum},
            ]

            var chart = AmCharts.makeChart("chartdiv", {
                "type": "serial",
                "theme": "light",
                "mouseWheelZoomEnabled": true,
                "dataProvider": Bought_report,
                "dataDateFormat": chart_date_format ,
                "valueAxes": [{
                    "id": "boughtAxis",
                    "gridColor": "#FFFFFF",
                    "gridAlpha": 0.2,
                    "dashLength": 0,
                    "position": "left",
                }],
                "gridAboveGraphs":
                    true,
                "startDuration":
                    1,
                "graphs": [{
                    "balloonText": " [[valueField]] <br><b style='font-size:20px;'>Bought: $ [[data_sum]] on [[date]]</b>",
                    // "fillAlphas": 0.3,
                    "lineAlpha": 0.5,
                    "bullet": "round",
                    "lineThickness": 3,
                    "bulletSize": 1,
                    "bulletBorderAlpha": 1,
                    "bulletColor": "#FFFFFF",
                    "useLineColorForBulletBorder": true,
                    "bulletBorderThickness": 3,
                    "valueField": "data_sum",
                    "valueAxis": "boughtAxis"
                },
                ],
                "chartCursor": {
                    "categoryBalloonEnabled":
                        false,
                    "cursorAlpha":
                        0,
                    "zoomable":
                        true
                }
                ,
                "categoryField": "date",
                "categoryAxis": {
                    "parseDates": true,
                    "dashLength": 1,
                    "minorGridEnabled": true,
                    "gridPosition": "start",
                    "gridAlpha": 0,
                    "tickPosition": "start",
                    "tickLength": 2
                },
                "export": {
                    "enabled":
                        true
                }
            });
        }
    });
}