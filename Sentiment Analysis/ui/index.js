function predictSentiment() {
    var url = "http://127.0.0.1:5000/predict";
    var input = document.getElementById("input_text");
    var result = document.getElementById("result");
    var senti = null;
    console.log('clicked')
    $.post(url, {
        input_text: input.value
    }, function(data, status){
        console.log(data.sentiment + " " + status);
        if (data.sentiment == "0") 
            senti = "Negative"
        else if (data.sentiment == "2")
            senti = "Neutral"
        else
            senti = "Positive" 
        result.innerHTML = "<h2>" + senti +"</h2>";
    });
    
}

