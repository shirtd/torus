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

    // mutex mtx;

    int index;
    set<Vertex*> adjacent;

    int simplex_index;
    set<int> nbrs;
    // set<Simplex*> nbrs;

    Vertex(Point<double,3> p, int i);
    ~Vertex();

    // void addsample(Point<double> p, Sample* s);
    bool is_adjacent(Vertex* v);
    bool is_adjacent(int i);

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

bool Vertex::is_adjacent(int i) {
    // lock_guard<recursive_mutex> guard(mutex);
    std::set<Vertex*>::iterator it;
    for (it = adjacent.begin(); it != adjacent.end(); ++it)
        if ((*it)->index == i) return true;
    return false;
}

class Edge {
public:
    Vertex* u;
    Vertex* v;
    // double time;
    int simplex_index;
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
    int index;
    double filtration;

    std::set<int> faces;
    // std::vector<int> col;

    std::set<int> incident;
    std::set<int> nbrs;

    // std::set<int> vertices;
    std::set<Vertex*> vertices;

    recursive_mutex mtx;

    bool ready;
    bool processed;

    condition_variable cv;

    Simplex(Vertex* v, int i);
    Simplex(std::set<int> f, int i, double filt);

    bool contains_vertex(int i);
    bool contains_vertex(Vertex* v);

    void add_vertices_to(Simplex* s);
    void add_incident_to(Simplex* s);
    void add_incident(int i);

    set<int> nbrs_containing(Vertex* v, vector<Simplex*> simplices);

    // int pc();
    // double* pcs();
};


Simplex::Simplex(Vertex* v, int i) {
    index = i;
    vertices.insert(v);
    filtration = 0;
    // time = v->time;
    dim = 0;
    ready = true;
    // processed = false;
}

Simplex::Simplex(std::set<int> f, int i, double filt) {
    faces = f;
    index = i;

    filtration = filt;

    dim = static_cast<int>(faces.size()-1);
    // set<int>::iterator it;
    // // for (int s : faces) {
    // for (it = faces.begin(); it != faces.end(); ++it) {
    //     col.push_back(*it);
    // }
    // std::sort(col.begin(), col.end());
    //    dim = vertices.size() - 1;
}

bool Simplex::contains_vertex(int i) {
    lock_guard<recursive_mutex> lock(mtx);

    std::set<Vertex*>::iterator it;
    for (it = vertices.begin(); it != vertices.end(); ++it )
        if ((*it)->index == i) return true;
    return false;
}

bool Simplex::contains_vertex(Vertex* v) {
    lock_guard<recursive_mutex> lock(mtx);

    std::set<Vertex*>::iterator it;
    for (it = vertices.begin(); it != vertices.end(); ++it)
        if (*it == v) return true;
    return false;
}

void Simplex::add_vertices_to(Simplex* s) {
    lock_guard<recursive_mutex> lock(mtx);

    set<Vertex*>::iterator vt;
    for (vt = vertices.begin(); vt != vertices.end(); ++vt)
        s->vertices.insert(*vt);
}
void Simplex::add_incident_to(Simplex* s) {
    lock_guard<recursive_mutex> lock(mtx);

    std::set_union(s->nbrs.begin(), s->nbrs.end(),
               incident.begin(), incident.end(),
               std::inserter(s->nbrs, s->nbrs.begin()));
}
void Simplex::add_incident(int i){
    lock_guard<recursive_mutex> lock(mtx);

    incident.insert(i);
}

set<int> Simplex::nbrs_containing(Vertex* v, vector<Simplex*> simplices){
    lock_guard<recursive_mutex> lock(mtx);

    std::set<int> tmp;
    set<int>::iterator nbrit;
    for (nbrit = nbrs.begin(); nbrit != nbrs.end(); ++nbrit) {
        if (simplices[*nbrit]->contains_vertex(v))
            tmp.insert(*nbrit);
    }
    return tmp;
}

#endif /* simplex_h */
