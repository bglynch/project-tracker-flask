/* global crossfilter, dc, d3, queue*/

/*-----------------------------------*/
/*---- Section 01: Load the Data ----*/
/*-----------------------------------*/
queue()
    .defer(d3.json, "./data")
    .await(makeGraphs);

/*----------------------------------------------------*/
/*---- Section 02: CROSSFILTER THE DATA AND PARSE ----*/
/*----------------------------------------------------*/
function makeGraphs(error, projectData) {
    var ndx = crossfilter(projectData);
    show_project_numbers(ndx);
    show_clients(ndx);
    dc.renderAll();
}

/*------------------------------------------------*/
/*---- Section 03: Create the Chart Finctions ----*/
/*------------------------------------------------*/

/*---- Number Displays: Total Porjects/TotalEarnings/Avg Value ----*/
function show_project_numbers(ndx) {
    var projectNumbers = ndx.groupAll().reduce(
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
                p.total -= v.project_value;
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
        .group(projectNumbers);
    
    dc.numberDisplay("#money_count")
        .valueAccessor(function(d) {
            if (d.count == 0) {
                return 0;
            }
            else {
                return d.total;
            }
        })
        .group(projectNumbers);
    
    dc.numberDisplay("#money_average")
        .valueAccessor(function(d) {
            if (d.count == 0) {
                return 0;
            }
            else {
                return d.average;
            }
        })
        .group(projectNumbers);
}

/*---- Row Charts: Clients ----*/
function show_clients(ndx) {
    var dim = ndx.dimension(dc.pluck('project_client'));
    var group = dim.group();

    dc.rowChart("#project-clients")
        .width(600)
        .height(330)
        .dimension(dim)
        .group(group)
        .elasticX(true)
        .xAxis().ticks(2)
        ;
}
