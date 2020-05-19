# 3D Landscape GeoMapper


## Python project for constructing 3D Landscape real-life surfaces and seeking shortest routes between points

### What is 3D Landscape GeoMapper?

It's an open source project built on Python and JavaScript that provides constuction and interactive visualization of 3D Landscape Model of any region of Earth's sphere. It have a lot of functions and features, for example finding the shortest path between two points throught the hard landscape. You can use a vast majority of kernel functions to regulate height, coverage and angle penalties to make route fit all you needs (for example Alpinism or Roads modeling). This project uses very accurate elevation dataset, taken from the sattelite with step 1 arcsecond, respectfuly it is an accuracy of 30 meters in practice. Naturally, the size of entire dataset is too huge to be gitted here, so I'm going to leave a reference on the resource, where you can download data with free access.

## Installation and Usage

### Source Code

```bash
$ git clone https://github.com/ViriAldi/HomeworkCycle2020
```

### Web Site

[PythonAnywhere](https://virialdi.pythonanywhere.com)

## Examples of work

* ### Plotting the K2 mountain landscape (Karakoram, Pakistan)

![k2](https://github.com/ViriAldi/HomeworkCycle2020/blob/master/examples/plot_examples/k2.png)

* ### Plotting the Masherbrum mountain landscape (Karakoram, Pakistan)

![masherbrum](https://github.com/ViriAldi/HomeworkCycle2020/blob/master/examples/plot_examples/masherbrum.png)

* ### Plotting the optimal path between Murren and mountain JungFrau (Alps, Swizerland)

![jungfrau](https://github.com/ViriAldi/HomeworkCycle2020/blob/master/examples/plot_examples/murren-jungfrau.png)

* ### Plotting the Annapurna I mountain landscape with high detalisation (Himalayas, Nepal)

![annapurna](https://github.com/ViriAldi/HomeworkCycle2020/blob/master/examples/plot_examples/annapurna.png)

* ### Plotting the optimal path between Pokhara and Annapurna I (Himalayas, Nepal)

![pokhara](https://github.com/ViriAldi/HomeworkCycle2020/blob/master/examples/plot_examples/annapurna-pokhara.png)

* ### Plotting the optimal road between Rakhiv and Yaremche (Carpathians, Ukraine)

![ukraine](https://github.com/ViriAldi/HomeworkCycle2020/blob/master/examples/plot_examples/rakhiv-yaremche.png)


# Input and Output data

The input data can be either geografical coordinates or name  of location (built-in geocoder will try to recognize the location and generate geografical coordinates for it), also you input size, quality and colormap. Program uses elevation dataset and then produces JavaScript interactive animation that is showed on the website, thats actual ouptut data.

# Project structure

## App

This is the directory with app implementation. There are:

* <b>app.py</b> - built on python Flask backend

* <b>tempaltes</b> - directory with html templates for web site

* <b>static</b> - directory with static files (images, css, javascipt, fonts)
  
## Examples

This is the directory with UML's of ADT and Data Structures and with working examples

## Structures

Python package with following modules:

* <b>lattice_adt.py</b> - module with implemented Lattice ADT

* <b>linked_array_data_structure.py</b> - module with implemented Array and Array2D Data Structures

* <b>node.py</b> - module with implemented Node ADT

## Geofiles

Directory with geofiles from dataset (just a few of them)

## Geocoder

Directory with geocoder (name -> coordinates and vice-versa) implementation on Python

## Mpl_3d

Directory with modules for transformation and computation Landscape and Pathes in Python

## Tiff_read

Directory with Python module for reading and transforming data to Lattice ADT


# Realization Details

## Modules

* Plotly.js

* Numpy

* Geopy

* Math

* Flask

* ctypes

* Pillow

* Heapq

## Details

For finding the path I used fast Dejkstra algorithm with priority queue, that gives time complexity O(nlogn), where n is area of the piece of landscape. Also the textures are dynamically scaled to achieve good and constant performance. You can implement the kernels you want to pass into path Lattice method to fit your needs.

### Path method

```python
    def path(self, point1, point2, kernel=Node.distance):
        """
        Finds the shortest path between two points of Lattice
        For distance measurement uses kernel function of two nodes
        By default it is distance function that penalizes height
        Uses Dejkstra Algorithm with priority queue. Complexity O(mlogn)
        :param point1: Node
        :param point2: Node
        :param kernel: function(Node, Node)
        :return: list of nodes
        """
```

### Dejkstra algorithm with priority queue (heap)

```python
        while li:
            node = heapq.heappop(li)
            if node.a != dist[node.b]:
                continue

            node = node.b
            if node == last:
                break

            for node_ in [node.n, node.e, node.s, node.w] + self.neighbours(node):
                if node_:
                    dst = kernel(node, node_)

                    if dist[node_] > dist[node] + dst:
                        parent[node_] = node
                        dist[node_] = dist[node] + dst
                        heapq.heappush(li, _Pair(dist[node_], node_))

        path = []
        node = last
        while node != first:
            path.append(node)
            node = parent[node]
        path.append(node)
  ```
  ### Example of plotting with Plotly.js
  
  ```javascript
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
```
