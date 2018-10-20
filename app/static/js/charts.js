/* global crossfilter, dc, d3, queue*/
//--------------------------------------------------- SECTION 01 - LOAD THE DATA
queue()
    .defer(d3.json, "http://project-tracker-flask-bglynch.c9users.io:8080/data")
    .await(makeGraphs);

//--------------------------------------------------- SECTION 02 - CROSSFILTER THE DATA AND PARSE
function makeGraphs(error, projectData) {
    var ndx = crossfilter(projectData);
    show_total_projects(ndx);
    show_project_numbers(ndx);
    show_clients(ndx);
    dc.renderAll();
}

//-- PIE CHARTS
function show_total_projects(ndx) {
    var dim = ndx.dimension(dc.pluck('user'));
    var group = dim.group();

    dc.pieChart("#total_projects")
        .height(250)
        .radius(100)
        .transitionDuration(100)
        .dimension(dim)
        .group(group)
        .minAngleForLabel(.2);
}

//-- NUMBER - AVERAGE HOUSE PRICE
function show_project_numbers(ndx) {
    var averageHousePrice = ndx.groupAll().reduce(
        function(p, v) {
            p.count++;
            p.total += v.project_value;
            p.average = p.total / p.count;
            return p;
        },
        function(p, v) {
            p.count--;
            if (p.count == 0) {
                p.total = 0;
                p.average = 0;
            }
            else {
                p.total -= v.price;
                p.average = p.total / p.count;
            }
            return p;
        },
        function() {
            return { count: 0, total: 0, average: 0 };
        }

    );

    dc.numberDisplay("#project_count")
        .valueAccessor(function(d) {
            if (d.count == 0) {
                return 0;
            }
            else {
                return d.count;
            }
        })
        .group(averageHousePrice);
    dc.numberDisplay("#money_count")
        .valueAccessor(function(d) {
            if (d.count == 0) {
                return 0;
            }
            else {
                return d.total;
            }
        })
        .group(averageHousePrice);
    dc.numberDisplay("#money_average")
        .valueAccessor(function(d) {
            if (d.count == 0) {
                return 0;
            }
            else {
                return d.average;
            }
        })
        .group(averageHousePrice);
}

//-- ROW CHART - PROPERTY AREAS
function show_clients(ndx) {
    var dim = ndx.dimension(dc.pluck('project_client'));
    var group = dim.group();

    dc.rowChart("#project-clients")
        .width(600)
        .height(330)
        .dimension(dim)
        .group(group)
        .elasticX(true)
        .xAxis().ticks(4);
}