//
//  simplex.h
//  tdsp
//
//  Created by kirk gardner on 4/14/17.
//  Copyright © 2017 kirk gardner. All rights reserved.
//

#ifndef simplex_h
#define simplex_h

#include "base.h"

class Vertex {
public:
    Point<double,3> point;
    // vector<Sample*> samples;
    // double time;

    int index;
    set<Vertex*> adjacent;

    phat::index simplex_index;
    set<phat::index> nbrs;
    // set<Simplex*> nbrs;

    Vertex(Point<double,3> p, int i);
    ~Vertex();

    // void addsample(Point<double> p, Sample* s);
    bool is_adjacent(Vertex* v);

    // double* pcs();
    // int pc();

};

Vertex::Vertex(Point<double,3> p, int i) {
    point = p;
    // samples.push_back(s);
    // time = s->time;
    index = i;
}

Vertex::~Vertex() {
    // std::cout << "\t\tdeleting samples ... ";
    // for (vector<Sample*>::iterator
    //         i = samples.begin(), e = samples.end();
    //         i != e; i++)
    //     delete (*i);
    // std::cout << "deleted samples." << std::endl;
}

bool Vertex::is_adjacent(Vertex* v) {
    std::set<Vertex*>::iterator it;
    for (it = adjacent.begin(); it != adjacent.end(); ++it)
        if (*it == v) return true;
    return false;
}

class Edge {
public:
    Vertex* u;
    Vertex* v;
    // double time;
    double filtration;

    Edge(Vertex* uu, Vertex* vv, double filt);
};

Edge::Edge(Vertex* uu, Vertex* vv, double filt) {
    u = uu;
    v = vv;
    filtration = filt;
    // if (u->time > v->time)
    //     time = u->time;
    // else time = v->time;
}

class Simplex {
public:
    int dim;
    // double time;
    phat::index index;
    double filtration;

    std::set<phat::index> faces;
    std::vector<phat::index> col;

    std::set<phat::index> incident;
    std::set<phat::index> nbrs;

    // std::set<int> vertices;
    std::set<Vertex*> vertices;

    Simplex(Vertex* v, phat::index i);
    Simplex(std::set<phat::index> f, phat::index i, double filt);

    bool contains_vertex(int i);
    bool contains_vertex(Vertex* v);

    // int pc();
    // double* pcs();
};


Simplex::Simplex(Vertex* v, phat::index i) {
    index = i;
    vertices.insert(v);
    filtration = 0;
    // time = v->time;
    dim = 0;
}

Simplex::Simplex(std::set<phat::index> f, phat::index i, double filt) {
    faces = f;
    index = i;

    filtration = filt;

    dim = static_cast<int>(faces.size()-1);
    set<phat::index>::iterator it;
    // for (phat::index s : faces) {
    for (it = faces.begin(); it != faces.end(); ++it) {
        col.push_back(*it);
    }
    std::sort(col.begin(), col.end());
    //    dim = vertices.size() - 1;
}

bool Simplex::contains_vertex(int i) {
    std::set<Vertex*>::iterator it;
    for (it = vertices.begin(); it != vertices.end(); ++it )
        if ((*it)->index == i) return true;
    return false;
}

bool Simplex::contains_vertex(Vertex* v) {
    std::set<Vertex*>::iterator it;
    for (it = vertices.begin(); it != vertices.end(); ++it)
        if (*it == v) return true;
    return false;
}

#endif /* simplex_h */
