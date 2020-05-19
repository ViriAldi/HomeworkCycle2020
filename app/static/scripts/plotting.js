function PlotMap(data_, colorscale){
    let data_x = data_[0];
    let data_y = data_[1];
    let data_z = data_[2];

    let data = [{
        x: data_x,
        y: data_y,
        z: data_z,
        type: 'surface',
        colorscale: colorscale,
        colorbar: {
            x: 1
        }
    }];

    let axis = {
        showgrid: false,
        zeroline: false,
        showline: false,
        autotick: true,
        ticks: '',
        showticklabels: false,
        title: {
            text: "",
            font: {size: 20, family: "myFirstFont", color: "black"}
        }
    };

    let layout = {
        autosize: false,
        width: 1322,
        height: 843,
        margin: {b: 0, t: 0, l: 0, r: 0,},
        scene: {
            camera: {
                center: {
                    z: -0.1
                },
                eye: {
                    z: 0.7,
                    x: 1.1,
                    y: 1.1
                }
            },
            aspectmode: "data",
            xaxis: axis,
            yaxis: axis,
            zaxis: axis,
        }
    };

    Plotly.plot('chart', data, layout);
}


function PlotPath(path){
    let path_x = path[0];
    let path_y = path[1];
    let path_z = path[2];

    let data = [{
            x: path_x,
            y: path_y,
            z: path_z,
            type: "scatter3d",
            mode: "lines",
            line: {
                width: 10,
                color: "black"
            }
        }];

    Plotly.plot('chart', data);
}