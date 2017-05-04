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
#include <chrono>

static const int threads = 8;

void _addcofaces(Graph* graph, vector<Edge*> toadd, int t, int j) {
// void _addcofaces(Graph* graph, Edge* e) {
    if (j < toadd.size()) {
        Edge* e = toadd[j];
        Simplex* s = graph->simplices[e->simplex_index];
        Vertex* u = e->u;
        Vertex* v = e->v;
        std::set<Vertex*> adjacent;
        std::set_intersection(u->adjacent.begin(), u->adjacent.end(),
                                v->adjacent.begin(), v->adjacent.end(),
                                std::inserter(adjacent,adjacent.begin()));
        graph->addcofaces(s, adjacent, e->filtration);
    }
}

int main(int argc, char * argv[]) {
    const char* name;
    if (argc > 1)
        name = argv[1];
    else name = "torus";

    string name_string = string(name);
    string filename_string = name_string+".txt";
    // filename = const_cast<char*>(filename_string.c_str());
    const char* filename = filename_string.c_str();
    // char* file = strtok(filename_copy, ".txt");

    cout << name << " (" << filename << ")" << endl;

    int dim = 2;
    // persistence over e?
    // (strict edge condition)
    double _e = 0.0;
    double _a = 0.0;

    double reso = 20;

    if (argc > 2) dim = strtod(argv[2], NULL);
    if (argc > 3) reso = strtod(argv[3],NULL);
    // if (argc > 2) _e = strtod(argv[3], NULL);
    // if (argc > 3) _a = strtod(argv[4], NULL);

    // cout << "_e = " << _e << endl;

    Graph* graph = new Graph(dim, _e, _a);

    ifstream infile(filename);
    double x,y,z;
    while (infile >> x >> y >> z) {
        Point<double,3> p;
        p[0] = x;
        p[1] = y;
        p[2] = z;
        graph->sample_vertex(p);
    } infile.close();

    int nvertices = graph->vertices.size();
    int nsimplices = graph->simplices.size();

    cout << nvertices << " vertices" << endl;
    cout << graph->simplices.size() << " simplices" << endl;

    // int added [nvertices][nvertices];
    // for (int i = 0; i < nvertices; i++) {
    //     std::fill(added[i], added[i]+nvertices, 0);
    // }

    vector<vector<Edge*>> added(reso);

    std::vector<std::thread> tt(threads);

    // REDUNDANT
    // each edge is only added once
    // -> generates cofaces
    // maintain a list of (2^nvertices) pairs ?
    // clock_t t1,t2;
    // t1=clock();
    auto start = chrono::steady_clock::now();
    //code goes here
    for (int i = 1; i < reso-2; i++) {

        double a = static_cast<double>(i)/(reso);
        cout << "_a = " << a << " ... ";
        graph->_a = a;
        for (int j = 0; j < nvertices; j++) {
            Vertex* u = graph->vertices[j];
            for (int k = j+1; k < nvertices; k++) {
                Vertex* v = graph->vertices[k];
                Edge* e = graph->sample_edge(u,v);
                if (e != nullptr) {
                    added[i].push_back(e);
                }
            }
        }

        // <editor-fold>
        // for (int j = 0; j < nvertices; j+=threads) {
        //     for (int k =j+1; k < nvertices; k+=1) {
        //         for (int t = 0; t < threads; t++) {
        //             tt[t] = thread(_addedge, graph, &added[i], t, j+t, k+t);
        //         }
        //         for(auto &e : tt) {
        //             e.join();
        //         }
        //     }
        // }
        // </editor-fold>

        cout << added[i].size() << " edges to add; ";

        for (int j = 0; j < added[i].size(); j+=threads) {
            for (int t = 0; t < threads-1; t++)
                tt[t] = thread(_addcofaces, graph, added[i], t, j+t);
            _addcofaces(graph, added[i], threads-1, j+threads-1);
            for(int t = 0; t < threads-1; t++) {
                if (tt[t].joinable())
                    tt[t].join();
            }
            // Edge* e = added[i][j];
            // Simplex* s = graph->simplices[e->simplex_index];
            // Vertex* u = e->u;
            // Vertex* v = e->v;
            // std::set<Vertex*> adjacent;
            // std::set_intersection(u->adjacent.begin(), u->adjacent.end(),
            //                         v->adjacent.begin(), v->adjacent.end(),
            //                         std::inserter(adjacent,adjacent.begin()));
            // graph->addcofaces(s, adjacent, e->filtration);
        }

        nsimplices = graph->simplices.size();
        cout << nsimplices << " simplices" << endl;
    }

    auto end = chrono::steady_clock::now();
    double elapsed = chrono::duration_cast<chrono::duration<double> >(end - start).count();
    // float diff ((float)t2-(float)t1);
    // float seconds = diff / CLOCKS_PER_SEC;
    cout << "build: " << elapsed << " seconds" << endl;

    clock_t t1,t2;
    t1=clock();

    graph->persist();

    t2=clock();
    float diff = ((float)t2-(float)t1);
    float seconds = diff / CLOCKS_PER_SEC;
    cout << "persist: " << seconds << " seconds" << endl;

    t1=clock();

    graph->write(name);

    t2=clock();
    diff = ((float)t2-(float)t1);
    seconds = diff / CLOCKS_PER_SEC;
    cout << "write: " << seconds << " seconds" << endl;

    delete graph;

    return 0;
}
