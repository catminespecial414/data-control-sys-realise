'use strict';
$(function() {
    chartA();
    chartB();
    chartC();
    chartD();
    chartE();
    chartF();
    chartG();
    chartK();
    chartH();
    chartJ();
    chartI();
    chartL();
    chartGG();
    chartGG2();
    chartGG3();
});

/* Basic Bar Chart  */
function chartC() {
    var options = {
        series: [{
            data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380]
        }],
        chart: {
            height: 350,
            type: 'bar',
            fontFamily: 'Poppins, sans-serif',
            toolbar: {
                show: false
            },
            zoom: {
                enabled: false
            },
        },
        plotOptions: {
            bar: {
                horizontal: true,
            }
        },
        dataLabels: {
            enabled: false
        },
        xaxis: {
            categories: ['South Korea', 'Canada', 'United Kingdom', 'Netherlands', 'Italy', 'France', 'Japan',
                'United States', 'China', 'Germany'
            ],
        },
        colors: ["#11a0fd"],
    };

    var chart = new ApexCharts(
        document.querySelector("#chartC"),
        options
    );

    chart.render();
}

/* Vertical Bar Chart */

function chartD() {

    var options = {
        chart: {
            height: 350,
            type: 'bar',
            fontFamily: 'Poppins, sans-serif',
            toolbar: {
                show: false
            },
            zoom: {
                enabled: false
            },
        },

        plotOptions: {
            bar: {
                dataLabels: {
                    position: 'top', // top, center, bottom
                },
            }
        },
        colors: ["#11a0fd"],
        dataLabels: {
            enabled: true,
            formatter: function(val) {
                return val + "%";
            },
            offsetY: -20,
            style: {
                fontSize: '12px',
                colors: ["#10163a"],
                fontFamily: 'Poppins, sans-serif',
            }
        },
        series: [{
            name: 'Revenue',
            data: [2.3, 3.1, 4.0, 10.1, 4.0, 3.6, 3.2, 2.3, 1.4, 0.8, 0.5, 0.2]
        }],
        xaxis: {
            categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            position: 'top',
            labels: {
                offsetY: -18,
                style: {
                    colors: '#10163a',
                    fontFamily: 'Poppins, sans-serif',
                }
            },
            axisBorder: {
                show: false
            },
            axisTicks: {
                show: false
            },
            crosshairs: {
                fill: {
                    type: 'gradient',
                    gradient: {
                        colorFrom: '#11a0fd',
                        colorTo: '#1b4962',
                        stops: [0, 100],
                        opacityFrom: 0.4,
                        opacityTo: 0.5,
                    }
                }
            },
            tooltip: {
                enabled: true,
                offsetY: -35,

            }
        },
        fill: {
            gradient: {
                shade: 'light',
                type: "horizontal",
                shadeIntensity: 0.25,
                gradientToColors: undefined,
                inverseColors: true,
                opacityFrom: 1,
                opacityTo: 1,
                stops: [50, 0, 100, 100]
            },
        },
        yaxis: {
            axisBorder: {
                show: false
            },
            axisTicks: {
                show: false,
            },
            labels: {
                show: false,
                formatter: function(val) {
                    return val + "%";
                }
            }

        },
        title: {
            text: 'Monthly Revenue',
            floating: true,
            offsetY: 320,
            align: 'center',
            style: {
                color: '#10163a',
                fontFamily: 'Poppins, sans-serif',
            }
        },
    }

    var chart = new ApexCharts(
        document.querySelector("#chartD"),
        options
    );

    chart.render();

}
/* Column Bar Chart */

function chartE() {
    var options = {
        chart: {
            fontFamily: 'Poppins, sans-serif',
            height: 350,
            type: 'bar',
            toolbar: {
                show: false
            },
            zoom: {
                enabled: false
            },
        },

        plotOptions: {
            bar: {
                horizontal: false,
                endingShape: 'rounded',
                columnWidth: '55%',
            },
        },
        dataLabels: {
            enabled: false,
        },
        stroke: {
            show: true,
            width: 2,
            colors: ['transparent'],
        },
        series: [{
            name: 'Net Profit',
            data: [44, 55, 57, 56, 61, 58, 63, 60, 66],

        }, {
            name: 'Revenue',
            data: [76, 85, 101, 98, 87, 105, 91, 114, 94],
        }, {
            name: 'Free Cash Flow',
            data: [35, 41, 36, 26, 45, 48, 52, 53, 41],
        }],
        legend: {
            show: true,
        },
        xaxis: {
            categories: ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
            labels: {
                style: {
                    colors: '#10163a',
                    fontFamily: 'Poppins, sans-serif',
                }
            }
        },
        yaxis: {
            title: {
                text: '$ (thousands)'
            },
            labels: {
                style: {
                    color: '#10163a',
                    fontFamily: 'Poppins, sans-serif',
                }
            }
        },
        fill: {
            opacity: 1,
        },
        tooltip: {
            y: {
                formatter: function(val) {
                    return "$ " + val + " thousands"
                }
            }
        },
        colors: ['#1b4962', '#ffa000', '#11a0fd']
    }

    var chart = new ApexCharts(
        document.querySelector("#chartE"),
        options
    );

    chart.render();
}

/* Column Bar Chart */

function chartF() {
    var options = {
        series: [{
            name: 'Marine Sprite',
            data: [44, 55, 41, 37, 22, 43, 21]
        }, {
            name: 'Striking Calf',
            data: [53, 32, 33, 52, 13, 43, 32]
        }, {
            name: 'Tank Picture',
            data: [12, 17, 11, 9, 15, 11, 20]
        }, {
            name: 'Bucket Slope',
            data: [9, 7, 5, 8, 6, 9, 4]
        }, {
            name: 'Reborn Kid',
            data: [25, 12, 19, 32, 25, 24, 10]
        }],
        chart: {
            type: 'bar',
            height: 350,
            stacked: true,
            toolbar: {
                show: false
            },
            zoom: {
                enabled: false
            },
        },
        plotOptions: {
            bar: {
                horizontal: true,
            },
        },
        stroke: {
            width: 1,
            colors: ['#fff']
        },
        title: {
            text: 'Fiction Books Sales'
        },
        xaxis: {
            categories: [2008, 2009, 2010, 2011, 2012, 2013, 2014],
            labels: {
                formatter: function(val) {
                    return val + "K"
                }
            }
        },
        yaxis: {
            title: {
                text: undefined
            },
        },
        tooltip: {
            y: {
                formatter: function(val) {
                    return val + "K"
                }
            }
        },
        fill: {
            opacity: 1
        },
        legend: {
            position: 'top',
            horizontalAlign: 'left',
            offsetX: 40
        },
        colors: ['#1b4962', '#ffa000', '#11a0fd', '#07a8ff', '#0b2354']
    };

    var chart = new ApexCharts(
        document.querySelector("#chartF"),
        options
    );

    chart.render();
}

/* Basic Line Chart */

function chartG() {
    var options = {
        chart: {
            height: 350,
            type: 'line',
            toolbar: {
                show: false
            },
            zoom: {
                enabled: false
            },
            shadow: {
                enabled: true,
                top: 18,
                left: 7,
                blur: 10,
                opacity: 1
            },
        },
        series: [{
            name: "Desktops",
            data: [10, 41, 35, 51, 49, 62, 69, 91, 148]
        }],

        dataLabels: {
            enabled: false
        },
        stroke: {
            curve: 'smooth'
        },
        title: {
            text: 'Product Trends by Month',
            align: 'left'
        },
        grid: {
            row: {
                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5
            },
        },
        xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
        },
        colors: ['#1b4962', '#ffa000']
    };


    var chart = new ApexCharts(
        document.querySelector("#chartG"),
        options
    );

    chart.render();
}

/* Line Chart with Data Labels */

function chartT() {
    var options = {
        chart: {
            height: 350,
            type: 'line',
            shadow: {
                enabled: true,
                color: '#111',
                top: 18,
                left: 7,
                blur: 10,
                opacity: 1
            },
            toolbar: {
                show: false
            },
            zoom: {
                enabled: false
            },
            fontFamily: 'Poppins, sans-serif',
        },
        colors: ['#1b4962', '#ffa000'],
        dataLabels: {
            enabled: true,
        },
        stroke: {
            curve: 'smooth'
        },
        series: [{
                name: "High - 2013",
                data: [28, 29, 33, 36, 32, 32, 33]
            },
            {
                name: "Low - 2013",
                data: [12, 11, 14, 18, 17, 13, 13]
            }
        ],
        title: {
            text: 'Average High & Low Temperature',
            align: 'left'
        },
        grid: {
            borderColor: '#e4e4e4',
            row: {
                colors: ['#f2f2f2', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5
            },
        },
        markers: {

            size: 6
        },
        xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            title: {
                text: 'Month'
            },
            labels: {
                style: {
                    colors: '#10163a',
                    fontFamily: 'Poppins, sans-serif',
                }
            }
        },
        yaxis: {
            title: {
                text: 'Temperature'
            },
            labels: {
                style: {
                    color: '#10163a',
                    fontFamily: 'Poppins, sans-serif',
                }
            },
            min: 5,
            max: 40
        },
        legend: {
            position: 'top',
            horizontalAlign: 'right',
            floating: true,
            offsetY: -25,
            offsetX: -5
        }
    }

    var chart = new ApexCharts(
        document.querySelector("#chartT"),
        options
    );

    chart.render();
}

/* Line & Column Chart */
function chartI() {
    var options = {
        chart: {
            height: 350,
            type: 'line',
            fontFamily: 'Poppins, sans-serif',
            toolbar: {
                show: false
            },
            zoom: {
                enabled: false
            },
        },
        series: [{
            name: 'Series1',
            type: 'column',
            data: [440, 505, 414, 671, 227, 413, 201, 352, 752, 320, 257, 160]
        }, {
            name: 'Series2',
            type: 'line',
            data: [23, 42, 35, 27, 43, 22, 17, 31, 22, 22, 12, 16]
        }],
        stroke: {
            width: [0, 4]
        },
        title: {
            text: 'Google Analytics'
        },
        labels: ['01 Jan 2020', '02 Jan 2020', '03 Jan 2020', '04 Jan 2020', '05 Jan 2020', '06 Jan 2020', '07 Jan 2020', '08 Jan 2020', '09 Jan 2020', '10 Jan 2020', '11 Jan 2020', '12 Jan 2020'],
        xaxis: {
            type: 'datetime',
            labels: {
                style: {
                    colors: '#10163a',
                    fontSize: '14px',
                    fontFamily: 'Poppins, sans-serif',
                }
            }
        },
        yaxis: [{
            title: {
                text: 'Website Blog',
            },
            labels: {
                style: {
                    color: '#10163a',
                }
            }

        }, {
            opposite: true,
            title: {
                text: 'Social Media'
            },
            labels: {
                style: {
                    color: '#10163a',
                }
            }
        }],
        colors: ['#1b4962', '#ffa000', '#11a0fd']

    }

    var chart = new ApexCharts(
        document.querySelector("#chartI"),
        options
    );

    chart.render();
}

/* Radial Chart */
function chartJ() {
    var options = {
        chart: {
            height: 350,
            type: 'radialBar',
            toolbar: {
                show: false
            },
            zoom: {
                enabled: false
            },
            fontFamily: 'Poppins, sans-serif',
        },
        plotOptions: {
            radialBar: {
                dataLabels: {
                    name: {
                        fontSize: '28px',
                    },
                    value: {
                        fontSize: '18px',
                    },
                    total: {
                        show: true,
                        label: 'Total',
                        formatter: function(w) {
                            // By default this function returns the average of all series. The below is just an example to show the use of custom formatter function
                            return 600
                        }
                    }
                }
            }
        },
        series: [44, 55, 67, 83],
        labels: ['Profit', 'Loss', 'Sales', 'Likes'],
        colors: ['#1b4962', '#ffa000', '#11a0fd', '#8dbf42']
    }

    var chart = new ApexCharts(
        document.querySelector("#chartJ"),
        options
    );

    chart.render();
}
/* Radar Chart  */

function chartK() {
    var options = {
        chart: {
            height: 350,
            type: 'radar',
            fontFamily: 'Poppins, sans-serif',
            dropShadow: {
                enabled: true,
                blur: 1,
                left: 1,
                top: 1
            },
            toolbar: {
                show: false
            },
            zoom: {
                enabled: false
            },
        },
        series: [{
            name: 'Series 1',
            data: [80, 50, 30, 40, 100, 20],
        }, {
            name: 'Series 2',
            data: [20, 30, 40, 80, 20, 80],
        }, {
            name: 'Series 3',
            data: [44, 76, 78, 13, 43, 10],
        }],
        title: {
            text: 'Radar Chart - Multi Series'
        },
        stroke: {
            width: 1
        },
        fill: {
            opacity: 0.4
        },
        markers: {
            size: 0
        },
        labels: ['2015', '2016', '2017', '2018', '2019', '2020'],
        colors: ['#1b4962', '#ffa000', '#11a0fd']
    }

    var chart = new ApexCharts(
        document.querySelector("#chartK"),
        options
    );

    chart.render();

    function update() {

        function randomSeries() {
            var arr = []
            for (var i = 0; i < 6; i++) {
                arr.push(Math.floor(Math.random() * 100))
            }

            return arr
        }

        chart.updateSeries([{
            name: 'Series 1',
            data: randomSeries(),
        }, {
            name: 'Series 2',
            data: randomSeries(),
        }, {
            name: 'Series 3',
            data: randomSeries(),
        }])
    }
}

/* Pie Chart */
function chartL() {
    var options = {
        chart: {
            width: 360,
            type: 'pie',
            fontFamily: 'Poppins, sans-serif',
            toolbar: {
                show: false
            },
            zoom: {
                enabled: false
            },
        },
        labels: ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'],
        series: [44, 55, 13, 43, 22],
        responsive: [{
            breakpoint: 480,
            options: {
                chart: {
                    width: 200
                },
                legend: {
                    position: 'bottom'
                }
            }
        }],
        colors: ['#1b4962', '#ffa000', '#11a0fd', '#8dbf42', '#5fc5ff']
    }

    var chart = new ApexCharts(
        document.querySelector("#chartL"),
        options
    );

    chart.render();
}

/* Widgets Chart */

function chartGG() {
    var options = {
        chart: {
            height: 300,
            type: 'line',
            toolbar: {
                show: false
            },
            zoom: {
                enabled: false
            },
            shadow: {
                enabled: true,
                top: 18,
                left: 7,
                blur: 10,
                opacity: 1
            },
        },
        series: [{
            name: "Desktops",
            data: [10, 41, 35, 51, 49, 62, 69, 91, 148]
        }],

        dataLabels: {
            enabled: false
        },
        stroke: {
            curve: 'smooth'
        },
        grid: {
            row: {
                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5
            },
        },
        xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
        },
        colors: ['#1b4962', '#ffa000']
    };


    var chart = new ApexCharts(
        document.querySelector("#chartGG"),
        options
    );

    chart.render();
}

function chartGG2() {
    var options = {
        chart: {
            height: 300,
            type: 'line',
            toolbar: {
                show: false
            },
            zoom: {
                enabled: false
            },
            shadow: {
                enabled: true,
                top: 18,
                left: 7,
                blur: 10,
                opacity: 1
            },

        },
        series: [{
            name: "Desktops",
            data: [10, 41, 35, 51, 49, 62, 69, 91, 148]
        }],

        dataLabels: {
            enabled: false
        },
        stroke: {
            curve: 'smooth'
        },
        grid: {
            row: {
                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5
            },
        },
        xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
        },
        colors: ['#1b4962', '#ffa000']
    };


    var chart = new ApexCharts(
        document.querySelector("#chartGG2"),
        options
    );

    chart.render();
}

function chartGG3() {
    var options = {
        chart: {
            height: 300,
            type: 'line',
            toolbar: {
                show: false
            },
            zoom: {
                enabled: false
            },
            shadow: {
                enabled: true,
                top: 18,
                left: 7,
                blur: 10,
                opacity: 1
            },
        },
        series: [{
            name: "Desktops",
            data: [10, 41, 35, 51, 49, 62, 69, 91, 148]
        }],

        dataLabels: {
            enabled: false
        },
        stroke: {
            curve: 'smooth'
        },
        grid: {
            row: {
                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5
            },
        },
        xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
        },
        colors: ['#1b4962', '#ffa000']
    };


    var chart = new ApexCharts(
        document.querySelector("#chartGG3"),
        options
    );

    chart.render();

}
// --- 1. 定义全局动态数据容器 ---
var timeLabels = [];
var ladybugData = [];
var mantisData = [];
var beetleData = [];

// --- 2. 重新定义 chartB 为动态图表 ---
function chartB() {
    var options = {
        chart: { 
            height: 350, 
            type: "area", 
            fontFamily: 'Poppins, sans-serif',
            animations: { enabled: true, easing: 'linear', dynamicAnimation: { speed: 1000 } },
            toolbar: { show: false }
        },
        // 初始化时数据为空
        series: [
            { name: "瓢虫类", data: [] }, 
            { name: "螳螂类", data: [] },
            { name: "甲虫类", data: [] }
        ],
        xaxis: { 
            categories: [],
            title: { text: '采集时间' },
            labels: { style: { colors: '#10163a' } }
        },
        stroke: { curve: 'smooth', width: 3 },
        colors: ['#00E396', '#FEB019', '#FF4560'], // 绿、橙、红
        dataLabels: { enabled: false }
    };

    // 将 chartB 实例挂载到 window 对象，方便外部 setInterval 访问
    window.pestChartInstance = new ApexCharts(document.querySelector("#chartB"), options);
    window.pestChartInstance.render();
}

// --- 3. 核心：每 5 秒联网抓取并更新 ---
setInterval(function() {
    fetch("/chart")
        .then(res => res.json())
        .then(data => {
            var now = new Date().toLocaleTimeString();
            
            // 压入新数据
            timeLabels.push(now);
            ladybugData.push(data.ladybug || 0);
            mantisData.push(data.mantis || 0);
            beetleData.push(data.beetle || 0);

            // 保持长度，防止图表太挤
            if (timeLabels.length > 15) {
                timeLabels.shift();
                ladybugData.shift();
                mantisData.shift();
                beetleData.shift();
            }

            // 执行更新
            if (window.pestChartInstance) {
                window.pestChartInstance.updateOptions({
                    xaxis: { categories: timeLabels }
                });
                window.pestChartInstance.updateSeries([
                    { name: "瓢虫类", data: ladybugData },
                    { name: "螳螂类", data: mantisData },
                    { name: "甲虫类", data: beetleData }
                ]);
            }
        })
        .catch(err => console.error("害虫数据拉取失败:", err));
}, 5000);