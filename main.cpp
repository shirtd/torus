//
//  main.cpp
//  tdsp
//
//  Created by kirk gardner on 4/6/17.
//  Copyright © 2017 kirk gardner. All rights reserved.
//

#include "graph.h"
#include <fstream>
#include <time.h>

int main(int argc, char * argv[]) {
    const char* filename;
    if (argc > 1)
        filename = argv[1];
    else filename = "torus.txt";

    std::string filename_string = std::string(filename);
    char* filename_copy = const_cast<char*>(filename_string.c_str());
    char* file = strtok(filename_copy, ".txt");

    cout << filename << " (" << file << ")" << endl;

    int dim = 2;
    // persistence over e?
    // (strict edge condition)
    double _e = 0.0;
    double _a = 0.0;

    if (argc > 2) _e = strtod(argv[2], NULL);
    if (argc > 3) _a = strtod(argv[3], NULL);
    if (argc > 4) dim = strtod(argv[4], NULL);

    cout << "_e = " << _e << endl;

    Graph* graph = new Graph(dim, _e, _a);

    // int nsamples = 14000;

    std::ifstream infile(filename);
    double x,y,z;
    while (infile >> x >> y >> z) {
        Point<double,3> p;
        p[0] = x;
        p[1] = y;
        p[2] = z;
        graph->sample_vertex(p);
    }

    int nvertices = graph->vertices.size();

    cout << nvertices << " vertices" << endl;
    // cout << graph->simplices.size() << endl;

    double added [nvertices][nvertices];

    // REDUNDANT
    // each edge is only added once
    // -> generates cofaces
    // maintain a list of (2^nvertices) pairs ?
    clock_t t1,t2;
    t1=clock();
    //code goes here
    double reso = 10;
    for (int i = 1; i < reso-2; i++) {
        double a = static_cast<double>(i)/(reso);
        cout << "_a = " << a << " ... ";
        graph->_a = a;
        for (int j = 0; j < nvertices; j++) {
            Vertex* u = graph->vertices[j];
            for (int k = j+1; k < nvertices; k++) {
                if (added[j][k] != 1) {
                    Vertex* v = graph->vertices[k];
                // if (!u->is_adjacent(v))
                    // graph->sample_edge(u,v);
                    if (graph->sample_edge(u,v) != nullptr) {
                        added[j][k] = 1;
                        added[k][j] = 1;
                    }
                }
            }
        }
        cout << graph->simplices.size() << " simplices" << endl;
    }

    t2=clock();
    float diff ((float)t2-(float)t1);
    float seconds = diff / CLOCKS_PER_SEC;
    cout << "build: " << seconds << " seconds" << endl;

    t1=clock();

    graph->persist();

    t2=clock();
    diff = ((float)t2-(float)t1);
    seconds = diff / CLOCKS_PER_SEC;
    cout << "persist: " << seconds << " seconds" << endl;

    t1=clock();

    graph->write(file);

    t2=clock();
    diff = ((float)t2-(float)t1);
    seconds = diff / CLOCKS_PER_SEC;
    cout << "write: " << seconds << " seconds" << endl;

    delete graph;

    return 0;
}
