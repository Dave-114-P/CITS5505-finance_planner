function getFlow(){
    console.log(flow);
    sumflow = flow['outflow'] - flow['inflow'];
    console.log(sumflow);
    $('#outflow_num').text(sumflow);
}

function budget(){
    
    let budgetWeekPercentage = (budgetWeek * 1.0).toFixed(1) + "%";

    console.log(budgetWeekPercentage)
    $('#progress-bar').css('width', budgetWeekPercentage);
    $('#progress-bar').text(budgetWeekPercentage);
}

getFlow()
budget()