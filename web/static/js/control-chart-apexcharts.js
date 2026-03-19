'use strict';

$(function() {
    // --- 任务清单：只保留页面上确实存在的图表 ---
    chartB(); // 你的害虫实时监测图表
    chartC(); 
    chartD();
    chartE();
    chartF();
    chartG();
    chartK();
    chartJ();
    chartI();
    chartL();
    
    // 如果你以后要在页面加上 GG 系列图表，再把下面这三行开头的 // 删掉
    // chartGG();
    // chartGG2();
    // chartGG3();
});

// --- 1. 你的核心功能：害虫实时监测图表 (chartB) ---
var timeLabels = [], lbData = [], mtData = [], btData = [];
window.pestChartInstance = null; 

function chartB() {
    var options = {
        chart: { 
            height: 350, 
            type: "area", 
            fontFamily: 'Poppins, sans-serif',
            toolbar: { show: false }
        },
        series: [
            { name: "瓢虫类", data: [] }, 
            { name: "螳螂类", data: [] },
            { name: "甲虫类", data: [] }
        ],
        xaxis: { categories: [], labels: { style: { colors: '#10163a' } } },
        stroke: { curve: 'smooth', width: 3 },
        colors: ['#00E396', '#FEB019', '#FF4560']
    };

    var domElement = document.querySelector("#chartB");
    if (domElement) {
        window.pestChartInstance = new ApexCharts(domElement, options);
        window.pestChartInstance.render();
    }
}

// 每5秒从后端 server.py 抓取一次害虫识别数据
setInterval(function() {
    if (!window.pestChartInstance) return; 

    fetch("/chart")
        .then(res => res.json())
        .then(data => {
            var now = new Date().toLocaleTimeString();
            timeLabels.push(now);
            lbData.push(data.ladybug || 0);
            mtData.push(data.mantis || 0);
            btData.push(data.beetle || 0);

            if (timeLabels.length > 15) {
                timeLabels.shift(); lbData.shift(); mtData.shift(); btData.shift();
            }

            window.pestChartInstance.updateOptions({
                xaxis: { categories: timeLabels },
                series: [
                    { name: "瓢虫类", data: lbData },
                    { name: "螳螂类", data: mtData },
                    { name: "甲虫类", data: btData }
                ]
            }, false, true); 
        })
        .catch(err => console.log("正在连接后端识别服务..."));
}, 5000);

// --- 2. 其他静态图表定义 (保持不变) ---

function chartC() {
    var options = {
        series: [{ data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380] }],
        chart: { height: 350, type: 'bar', fontFamily: 'Poppins, sans-serif', toolbar: { show: false } },
        plotOptions: { bar: { horizontal: true } },
        xaxis: { categories: ['韩', '加', '英', '荷', '意', '法', '日', '美', '中', '德'] },
        colors: ["#11a0fd"],
    };
    var dom = document.querySelector("#chartC");
    if(dom) new ApexCharts(dom, options).render();
}

function chartD() {
    var options = {
        chart: { height: 350, type: 'bar', fontFamily: 'Poppins, sans-serif', toolbar: { show: false } },
        series: [{ name: 'Revenue', data: [2.3, 3.1, 4.0, 10.1, 4.0, 3.6, 3.2, 2.3, 1.4, 0.8, 0.5, 0.2] }],
        xaxis: { categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] },
        colors: ["#11a0fd"]
    };
    var dom = document.querySelector("#chartD");
    if(dom) new ApexCharts(dom, options).render();
}

function chartE() {
    var options = {
        chart: { height: 350, type: 'bar', toolbar: { show: false } },
        series: [{ name: 'Net Profit', data: [44, 55, 57, 56, 61, 58, 63, 60, 66] }, 
                 { name: 'Revenue', data: [76, 85, 101, 98, 87, 105, 91, 114, 94] }],
        xaxis: { categories: ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'] },
        colors: ['#1b4962', '#ffa000']
    };
    var dom = document.querySelector("#chartE");
    if(dom) new ApexCharts(dom, options).render();
}

function chartF() {
    var options = {
        series: [{ name: 'Marine Sprite', data: [44, 55, 41, 37, 22, 43, 21] }],
        chart: { type: 'bar', height: 350, stacked: true, toolbar: { show: false } },
        xaxis: { categories: [2008, 2009, 2010, 2011, 2012, 2013, 2014] },
        colors: ['#1b4962']
    };
    var dom = document.querySelector("#chartF");
    if(dom) new ApexCharts(dom, options).render();
}

function chartG() {
    var options = {
        chart: { height: 350, type: 'line', toolbar: { show: false } },
        series: [{ name: "Desktops", data: [10, 41, 35, 51, 49, 62, 69, 91, 148] }],
        xaxis: { categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'] },
        colors: ['#1b4962']
    };
    var dom = document.querySelector("#chartG");
    if(dom) new ApexCharts(dom, options).render();
}

function chartI() {
    var options = {
        chart: { height: 350, type: 'line', toolbar: { show: false } },
        series: [{ name: 'Series1', type: 'column', data: [440, 505, 414, 671, 227] }, 
                 { name: 'Series2', type: 'line', data: [23, 42, 35, 27, 43] }],
        labels: ['01 Jan 2020', '02 Jan 2020', '03 Jan 2020', '04 Jan 2020', '05 Jan 2020'],
        xaxis: { type: 'datetime' },
        colors: ['#1b4962', '#ffa000']
    };
    var dom = document.querySelector("#chartI");
    if(dom) new ApexCharts(dom, options).render();
}

function chartJ() {
    var options = {
        chart: { height: 350, type: 'radialBar' },
        series: [44, 55, 67, 83],
        labels: ['Profit', 'Loss', 'Sales', 'Likes'],
        colors: ['#1b4962', '#ffa000', '#11a0fd', '#8dbf42']
    };
    var dom = document.querySelector("#chartJ");
    if(dom) new ApexCharts(dom, options).render();
}

function chartK() {
    var options = {
        chart: { height: 350, type: 'radar', toolbar: { show: false } },
        series: [{ name: 'Series 1', data: [80, 50, 30, 40, 100, 20] }],
        labels: ['2015', '2016', '2017', '2018', '2019', '2020'],
        colors: ['#1b4962']
    };
    var dom = document.querySelector("#chartK");
    if(dom) new ApexCharts(dom, options).render();
}

function chartL() {
    var options = {
        chart: { width: 360, type: 'pie' },
        labels: ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'],
        series: [44, 55, 13, 43, 22],
        colors: ['#1b4962', '#ffa000', '#11a0fd', '#8dbf42', '#5fc5ff']
    };
    var dom = document.querySelector("#chartL");
    if(dom) new ApexCharts(dom, options).render();
}