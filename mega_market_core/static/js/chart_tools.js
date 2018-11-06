function chart_tools(filters_to_apply) {
    var current_date = new Date();
    var current_year = current_date.getFullYear();
    var current_month = current_date.getMonth();
    var current_day = current_date.getDate();
    $.ajax({
        method: "GET",
        url: 'http://127.0.0.1:8000/api/earnedboughtsold/',
        data: filters_to_apply,
        success: function (data) {

            console.log(data)

            var Earned_report = data.earned_report_chart
            var Bought_report = data.bought_report_chart
            var Sold_report = data.sold_report_chart

            $(".empty_message").empty()

            if (Earned_report === undefined || Earned_report.length === 0){
                Earned_report =[{'date': '2000-01-01', 'data_sum': 0},]
                $('#earnedtitlediv').append('<p class="empty_message" style="font-size: 14px">(empty)</p>')
            }
            if (Bought_report === undefined || Bought_report.length === 0){
                Bought_report =[{'date': '2000-01-01', 'data_sum': 0},]
                $('#boughttitlediv').append('<p class="empty_message">(empty)</p>')
            }
            if (Sold_report === undefined || Sold_report.length === 0){
                Sold_report =[{'date': '2000-01-01', 'data_sum': 0},]
                $('#soldtitlediv').append('<p class="empty_message">(empty)</p>')
            }

            make_chart(
                Earned_report,
                data.chart_date_format,
                "earnedchartdiv",
                filters_to_apply.date__gt,
                filters_to_apply.date__lt,
            )
            make_chart(
                Bought_report,
                data.chart_date_format,
                "boughtchartdiv",
                filters_to_apply.date__gt,
                filters_to_apply.date__lt,
            )
            make_chart(
                Sold_report,
                data.chart_date_format,
                "soldchartdiv",
                filters_to_apply.date__gt,
                filters_to_apply.date__lt,
            )
        }
    });
}

function make_chart(chart_data, time_format, chart_div_id, start_date, end_date) {

    var chart = AmCharts.makeChart(chart_div_id, {
        "type": "serial",
        "theme": "light",
        "mouseWheelZoomEnabled": true,
        "dataProvider": chart_data,
        "dataDateFormat": time_format,
        "valueAxes": [{
            "position": "bottom",
            "offset": 0,
            "minimum": start_date,
            "maximum": end_date
            // "minimum": 2,
            // "maximum": 6
        }, {
            "id": "valueAxis",
            "gridColor": "#FFFFFF",
            "gridAlpha": 0.2,
            "dashLength": 0,
            "position": "left",
        }],
        "gridAboveGraphs":
            true,
        "startEffect": "easeOutSine",
        "startDuration": 0.25,
        "responsive": {
            "enabled": true
        },
        "graphs": [{
            "balloonText": " [[valueField]] <br><b style='font-size:20px;'>$ [[data_sum]] : [[date]]</b>",
            "fillAlphas": 0.3,
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
            "minPeriod": "mm",
            "minorGridEnabled": true,
            "gridPosition": "start",
            "gridAlpha": 0,
            "tickPosition": "start",
            "tickLength": 2
        },
        "export": {
            "enabled":
                false
        }
    });
}