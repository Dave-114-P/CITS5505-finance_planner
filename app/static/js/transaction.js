function getFlow(){
    console.log(flow);
    let parsedFlow = JSON.parse(flow)
    console.log(parsedFlow);
    console.log('type: ', typeof(parsedFlow));
    // console.log('type: ', typeof(parsedFlow['outflows']));
    let sumflow = (parsedFlow.outflow - parsedFlow.inflow).toFixed(1);
    console.log(sumflow);
    $('#sumflow_num').text(sumflow);
}

function budget(){
    
    let budgetWeekPercentage = (budgetWeek * 1.0).toFixed(1) + "%";

    console.log(budgetWeekPercentage)
    $('#progress-bar').css('width', budgetWeekPercentage);
    $('#progress-bar').text(budgetWeekPercentage);
}

getFlow()
budget()