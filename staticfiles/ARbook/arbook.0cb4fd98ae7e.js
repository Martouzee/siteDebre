
document.addEventListener('DOMContentLoaded', function() {
    interneSelect = document.querySelector('#internes');
    choiceSelect = document.querySelector('#geste');
    chirSelect = document.querySelector('#chirurgies');
    let interneId;
    let choiceId;
    let chirId
    let graph = null

    interneSelect.addEventListener('change', () => {
        interneId = interneSelect.value
        clearDiv();
        graphRepart(interneId)
    });
    choiceSelect.addEventListener('change', () => {
        choiceId = choiceSelect.value
        clearDiv();
        graphGeste(choiceId)
    });
    chirSelect.addEventListener('change', () => {
        chirId = chirSelect.value
        clearDiv();
        graphChir(chirId)
    });
});

function graphRepart(interne) {
    let div = document.getElementById('repartition');
    div.innerHTML = '';

    fetch(`/view-interne/${interne}`)
    .then(response => response.json())
    .then(data => {
        for (let key in data) {
            //create a graph for each logical key (!= 'internes')
            //Select all the key
            if (key != 'Interne'){
                console.log(key)
                // for all inner key 
                //create the labels
                labelsList = Object.keys(data[key])
                //create the data table
                let interneData = []
                let moyenneData = []
                let diffData = []
                for (let innerKey in data[key]) {
                    //for each Innerkey push the data 
                    let results = data[key][innerKey];
                    interneData.push(results.perso);
                    moyenneData.push(results.moyenne);
                    diffData.push(results.difference);
                    }
                //create the dataGraph
                const graphData = {
                    labels: labelsList,
                    datasets: [
                        {
                        label: 'Interne',
                        data: interneData,
                        stack: 'combined',
                        type: 'bar'
                        },
                        {
                        label: 'Moyenne',
                        data: moyenneData,
                        stack: 'combined'
                        },
                        {
                        label: 'Difference',
                        data: diffData,
                        stack: 'combined'
                        }
                    ]
                }
                //create the congig
                const config = {
                    type: 'line',
                    data: graphData,
                    options: {
                        plugins: {
                        title: {
                            display: true,
                            text: key
                        },
                        },
                        responsive: true,
                        scales: {
                        y: {
                            stacked: false
                        }
                        }
                    }
                }
                //Create a div with the graph
                canvas = document.createElement('canvas')
                canvas.id = `graph-${key}`
                div.append(canvas)
                var ctx = document.getElementById(`graph-${key}`).getContext('2d');
                var graph = new Chart(ctx, config);
            }


        }
    })
}

function graphGeste(geste) {
    console.log(geste)
    let div = document.getElementById('comparaison');
    div.innerHTML = '';
    canvas = document.createElement('canvas')
    canvas.id = 'graph2'
    div.append(canvas)

    // Get the labels
    let interneData = []
    let moyenneData = []
    let diffData = []

    const fetchRequests = labels.map(interne => {
        return fetch(`/view-interne/${interne}`)
            .then(response => response.json());
    });
        
    Promise.all(fetchRequests).then(responses => {
        responses.forEach(data => {
            for (let key in data) {
                for (let innerKey in data[key]) {
                    if (innerKey == geste) {
                        let results = data[key][innerKey];
                        interneData.push(results.perso);
                        moyenneData.push(results.moyenne);
                        diffData.push(results.difference);
                    }
                }
            }
            })    
    });

    Promise.all(fetchRequests)
    .then(() => {
    // Create the graph
    var ctx = document.getElementById('graph2').getContext('2d');

    const dataGraph = {
        labels: labels,
        datasets: [
            {
            label: 'Interne',
            data: interneData,
            stack: 'combined',
            type: 'bar'
            },
            {
            label: 'Moyenne',
            data: moyenneData,
            stack: 'combined'
            },
            {
            label: 'Difference',
            data: diffData,
            stack: 'combined'
            }
        ]
        };

    const config = {
        type: 'line',
        data: dataGraph,
        options: {
            plugins: {
            title: {
                display: true,
                text: geste
            },
            },
            responsive: true,
            scales: {
            y: {
                stacked: false
            }
            }
        }
        };
        


    var graph2 = new Chart(ctx, config);
    })
};

function graphChir(chirChoice) {
    let div = document.getElementById('chir');
    div.innerHTML = '';
    canvas = document.createElement('canvas')
    canvas.id = 'graph3'
    div.append(canvas)
    // Get the labels
    let interneData = []
    let moyenneData = []
    let diffData = []

    const fetchRequests = labels.map(interne => {
        return fetch(`/view-interne/${interne}`)
            .then(response => response.json());
    });
        
    Promise.all(fetchRequests).then(responses => {
        responses.forEach(data => {
            let chirurgies = data['Chirurgies']
            Object.keys(data['Chirurgies']).map(chir => { 
                if (chir == chirChoice) {
                    let results = chirurgies[chir]
                    interneData.push(results.perso);
                    moyenneData.push(results.moyenne);
                    diffData.push(results.difference);
                }
        })
            })    
    });

    Promise.all(fetchRequests)
    .then(() => {
    // Create the graph
    var ctx = document.getElementById('graph3').getContext('2d');

    const dataGraph = {
        labels: labels,
        datasets: [
            {
            label: 'Interne',
            data: interneData,
            stack: 'combined',
            type: 'bar'
            },
            {
            label: 'Moyenne',
            data: moyenneData,
            stack: 'combined'
            },
            {
            label: 'Difference',
            data: diffData,
            stack: 'combined'
            }
        ]
        };

    const config = {
        type: 'line',
        data: dataGraph,
        options: {
            plugins: {
            title: {
                display: true,
                text: chirChoice
            },
            },
            responsive: true,
            scales: {
            y: {
                stacked: false
            }
            }
        }
        };
        


    var graph3 = new Chart(ctx, config);
    })
};

function clearDiv() {
    document.getElementById('repartition').innerHTML = '';
    document.getElementById('comparaison').innerHTML='';
    document.getElementById('chir').innerHTML = '';
}
/*     fetch(`/view-interne/${interne}`)
    .then(response => response.json())
    .then(data => {


        // Get the labels
        const labels = Object.keys(data.chirurgies)
        
        // Get the Interne Data
        const interneData = Object.values(data.chirurgies).map((item) => item.perso);

        // Get the Moyenne Data
        const moyenneData = Object.values(data.chirurgies).map((item) => item.moyenne);

        // Get the Difference Data
        const diffData = Object.values(data.chirurgies).map((item) => item.difference);


        // Create the graph
        var ctx = document.getElementById('graph1').getContext('2d');

        const dataGraph = {
            labels: labels,
            datasets: [
              {
                label: interne,
                data: interneData,
                stack: 'combined',
                type: 'bar'
              },
              {
                label: 'Moyenne',
                data: moyenneData,
                stack: 'combined'
              },
              {
                label: 'Difference',
                data: diffData,
                stack: 'combined'
              }
            ]
          };

        const config = {
            type: 'line',
            data: dataGraph,
            options: {
              plugins: {
                title: {
                  display: true,
                  text: 'Repartition des chirurgies'
                },
              },
              responsive: true,
              scales: {
                y: {
                  stacked: false
                }
              }
            }
          };
          


        var graph1 = new Chart(ctx, config);
    }); */