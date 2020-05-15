console.log({{ time }})
Plotly.d3.csv('static/data_x.csv', function(err,rows) {
    var data_x = [];
    for (let i = 0; i < rows.length; i++) {
        data_x.push(rows.map(row => row [i]));
    }
    Plotly.d3.csv('static/data_y.csv', function (err, rows) {
        var data_y = [];
        for (let i = 0; i < rows.length; i++) {
            data_y.push(rows.map(row => row [i]));
        }
        Plotly.d3.csv('static/data_z.csv', function (err, rows) {
            var data_z = [];
            for (let i = 0; i < rows.length; i++) {
                data_z.push(rows.map(row => row [i]));
            }
            Plotly.d3.csv('static/data_path.csv', function (err, rows) {
                let x_path = [];
                let y_path = [];
                let z_path = [];

                for (let i = 0; i < 400; i++){
                    x_path.push(rows[0][i]);
                    y_path.push(rows[1][i]);
                    z_path.push(rows[2][i]);
                }

                let data = [{
                        x: data_x,
                        y: data_y,
                        z: data_z,
                        type: 'surface',
                        colorscale: "Earth",
                    },
                    {
                        x: x_path,
                        y: y_path,
                        z: z_path,
                        type: "scatter3d",
                        mode: "lines",
                        line: {
                            width: 6,
                            color: "black",
                        }
                    }];

                let layout = {
                    title: 'Landscape',
                    autosize: false,
                    width: 2000,
                    height: 800,
                    margin: {
                        l: 300,
                        r: 300,
                        b: 0,
                        t: 100,
                    },
                    scene: {
                        aspectmode: "data"
                    }
                };

                Plotly.plot('chart', data, layout);
            })
        })
    })
});
