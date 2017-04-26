//
//  graph.h
//  tdsp
//
//  Created by kirk gardner on 4/14/17.
//  Copyright © 2017 kirk gardner. All rights reserved.
//

#ifndef graph_h
#define graph_h

#include "simplex.h"

typedef pair<int,int> pair_t;

struct feature_t {
    int index;
    pair_t pair;
};

class Graph {
public:
    int dim;

    double _e;
    double _a;

    std::vector<Vertex*> vertices;
    std::vector<Edge*> edges;
    std::vector<Simplex*> simplices;

    phat::boundary_matrix< phat::vector_vector > boundary_matrix;
    phat::persistence_pairs pairs;
    vector<feature_t> features;

    mutex mtx;

    Graph(int d, double e, double a);
    ~Graph();

    Vertex* sample_vertex(Point<double,3> p);
    Edge* sample_edge(Vertex* u, Vertex* v);

    void persist();

    void write(const char* file);

    Simplex* gensimplex(std::set<int> s, double filt);
    vector<Simplex*> getcofaces(Simplex* s, std::set<Vertex*> adjacent, double filt);

    void addcofaces(Simplex* s, std::set<Vertex*> adjacent, double filt);

 private:

    Vertex* addvertex(Point<double,3> p);
    Edge* addedge(Vertex* u, Vertex* v);
    Simplex* addsimplex(Vertex* v);
    Simplex* addsimplex(std::set<int> s, double filt);

    void write_vertices(char* path);
    void write_edges(char* path);
    void write_simplices(char* path);
    void write_boundary(char* path);
    void write_pairs(char* path);
    void write_stats(char* path);
};

Graph::Graph(int d, double e, double a) {
    dim = d;
    _e = e;
    _a = a;
}

Graph::~Graph() {
    // std::cout << "\tdeleting vertices ... ";
    for (vector<Vertex*>::iterator
         i = vertices.begin(), e = vertices.end();
         i != e; ++i)
        delete (*i);
    // std::cout << "deleted vertices." << std::endl;

    // std::cout << "\tdeleting edges ... " << std::endl;
    for (vector<Edge*>::iterator
         i = edges.begin(), e = edges.end();
         i != e; ++i)
        delete (*i);
    // std::cout << "deleted edges." << std::endl;

    for (vector<Simplex*>::iterator
         i = simplices.begin(), e = simplices.end();
         i != e; ++i)
        delete (*i);
}

Vertex* Graph::sample_vertex(Point<double,3> p) {
    return addvertex(p);
}

Vertex* Graph::addvertex(Point<double,3> p) {
    int n = static_cast<int>(vertices.size());
    Vertex* v = new Vertex(p, n);
    vertices.push_back(v);
    Simplex* sim = addsimplex(v);
    v->simplex_index = sim->index;
    return v;
}

Edge* Graph::sample_edge(Vertex* u, Vertex* v) {
    if ((u == nullptr || v == nullptr) || (u == v)) return nullptr;
    if (!u->is_adjacent(v)) {
        double d = dist3(u->point,v->point);
        if (d < _a) {
            return addedge(u, v);
        }
    }

    return nullptr;
}

Edge* Graph::addedge(Vertex* u, Vertex* v) {
    double d = dist3(u->point,v->point);
    Edge* e = new Edge(u, v, d);

    u->adjacent.insert(v);
    v->adjacent.insert(u);
    edges.push_back(e);

    set<int> tmp;
    tmp.insert(u->simplex_index);
    tmp.insert(v->simplex_index);
    Simplex* s = addsimplex(tmp, d);
    e->simplex_index = s->index;
    // std::set<Vertex*> adjacent;
    // std::set_intersection(u->adjacent.begin(), u->adjacent.end(),
    //                         v->adjacent.begin(), v->adjacent.end(),
    //                         std::inserter(adjacent,adjacent.begin()));
    // addcofaces(s,adjacent,d);
    return e;
}

Simplex* Graph::gensimplex(std::set<int> f, double filt) {
    Simplex* s = new Simplex(f, -1, filt);
    set<int>::iterator it;
    for(it = s->faces.begin(); it != s->faces.end(); ++it) {
        set<Vertex*>::iterator vt;
        for (vt = simplices[*it]->vertices.begin();
             vt != simplices[*it]->vertices.end(); ++vt)
            s->vertices.insert(*vt);
        std::set_union(s->nbrs.begin(), s->nbrs.end(),
                       simplices[*it]->incident.begin(), simplices[*it]->incident.end(),
                       std::inserter(s->nbrs, s->nbrs.begin()));
    }

    if (s->vertices.size() == s->dim+1) {
        set<int>::iterator it;
        for (it = s->faces.begin(); it != s->faces.end(); ++it)
            simplices[simplices[*it]->index]->incident.insert(s->index);

        // simplices.push_back(s);
    }

    return s;
}

Simplex* Graph::addsimplex(Vertex* v) {
    Simplex* s = new Simplex(v, simplices.size());
    // for (int i : vertices[i].adjacent)
    set<Vertex*>::iterator it;
    for (it = v->adjacent.begin();
         it != v->adjacent.end(); ++it)
        s->nbrs.insert((*it)->simplex_index);
    // lock_guard<mutex> guard(mutex);
    simplices.push_back(s);
    return s;
}

Simplex* Graph::addsimplex(std::set<int> f, double filt) {
    Simplex* s = new Simplex(f, simplices.size(), filt);
    // lock_guard<mutex> block_threads_until_finish_this_job(mtx);
    set<int>::iterator it;
    for(it = s->faces.begin(); it != s->faces.end(); ++it) {
        Simplex* t = simplices[*it];

        t->add_vertices_to(s);
        // set<Vertex*>::iterator vt;
        // for (vt = t->vertices.begin();
        //      vt != t->vertices.end(); ++vt)
        //     s->vertices.insert(*vt);

        t->add_incident_to(s);
        // std::set_union(s->nbrs.begin(), s->nbrs.end(),
        //                t->incident.begin(), t->incident.end(),
        //                std::inserter(s->nbrs, s->nbrs.begin()));
    }

    if (s->vertices.size() == s->dim+1) {
        set<int>::iterator it;
        for (it = s->faces.begin(); it != s->faces.end(); ++it) {
            Simplex* t = simplices[*it];

            t->add_incident(s->index);
            // t->incident.insert(s->index);
        }
        mtx.lock();
        simplices.push_back(s);
        mtx.unlock();
    }

    return s;
}

void Graph::addcofaces(Simplex* s, std::set<Vertex*> adjacent, double filt) {
    if (s->dim >= dim) return;
    // lock_guard<recursive_mutex> lock(s->mtx);
    set<Vertex*>::iterator adjit;
    for (adjit = adjacent.begin(); adjit != adjacent.end(); ++adjit) {
        // std::set<int> tmp = s->nbrs_containing(*adjit, simplices);
        s->mtx.lock();
        std::set<int> tmp;
        set<int>::iterator nbrit;
        for (nbrit = s->nbrs.begin(); nbrit != s->nbrs.end(); ++nbrit) {
            if (simplices[*nbrit]->contains_vertex(*adjit))
                tmp.insert(*nbrit);
        }
        s->mtx.unlock();
        if (tmp.size() == s->dim+1) {
            tmp.insert(s->index);
            // lock_guard<std::mtx> block_threads_until_finish_this_job(mtx);
            Simplex* t = addsimplex(tmp, filt);
            if (t->vertices.size() != t->dim+1) return;
            std::set<Vertex*> adj;
            std::set_intersection(adjacent.begin(), adjacent.end(),
                           (*adjit)->adjacent.begin(), (*adjit)->adjacent.end(),
                           std::inserter(adj,adj.begin()));
            addcofaces(t, adj, filt);
        }
    }
}

// vector<Simplex*> Graph::getcofaces(Simplex* s, std::set<Vertex*> adjacent, double filt) {
//     vector<Simplex*> toadd;
//     if (s->dim >= dim) return toadd;
//
//     set<Vertex*>::iterator adjit;
//     for (adjit = adjacent.begin(); adjit != adjacent.end(); ++adjit) {
//         std::set<int> tmp;
//
//         set<int>::iterator nbrit;
//         for (nbrit = s->nbrs.begin(); nbrit != s->nbrs.end(); ++nbrit) {
//             if (simplices[*nbrit]->contains_vertex(*adjit))
//                 tmp.insert(*nbrit);
//         }
//
//         if (tmp.size() == s->dim+1) {
//             tmp.insert(s->index);
//             Simplex* t = gensimplex(tmp, filt);
//             if (t->vertices.size() != t->dim+1) return toadd;
//             toadd.push_back(t);
//             std::set<Vertex*> adj;
//             std::set_intersection(adjacent.begin(), adjacent.end(),
//                            (*adjit)->adjacent.begin(), (*adjit)->adjacent.end(),
//                            std::inserter(adj,adj.begin()));
//             vector<Simplex*> _toadd = getcofaces(t, adj, filt);
//             toadd.insert(toadd.end(), _toadd.begin(), _toadd.end());
//             return toadd;
//         }
//     }
//
//     return toadd;
// }

void Graph::persist() {
    int nsimplices = simplices.size();
    boundary_matrix.set_num_cols(nsimplices);
    for (int i = 0; i < nsimplices; i++) {
        Simplex* s = simplices[i];
        vector<phat::index> col;
        set<int>::iterator it;
        // for (int s : faces) {
        for (it = s->faces.begin(); it != s->faces.end(); ++it)
            col.push_back(static_cast<phat::index>(*it));
        std::sort(col.begin(), col.end());
        boundary_matrix.set_dim(s->index, s->dim);
        boundary_matrix.set_col(s->index, col);
    }

    // choose an algorithm (choice affects performance) and compute the persistence pair
    // (modifies boundary_matrix)
    phat::compute_persistence_pairs< phat::twist_reduction >( pairs, boundary_matrix);

    // sort the persistence pairs by birth index
    // pairs.sort();

    // int count = 0;
    for( int idx = 0; idx < pairs.get_num_pairs(); idx++ ) {
        pair_t pair = pairs.get_pair(idx);
        if (pair.second - pair.first > PERS_THRESH) {
            feature_t feature;
            feature.index = idx;
            feature.pair = pair;
            features.push_back(feature);
        }
    }
}

// <editor-fold> write
void Graph::write(const char* file) {
    string data_dir_string = "data/";
    const char* data_dir = data_dir_string.c_str();
    if (!dir_exists(data_dir)) _mkdir(data_dir);

    // int i = 0;
    // string file_dir_suffix_string = "_" +
    //         // to_string_double(_e) + "_" +
    //         // to_string_double(_a) + "_" +
    //         to_string(i);

    // const char* file_dir_suffix = file_dir_suffix_string.c_str();
    // int length = strlen(data_dir)+strlen(file)+strlen(file_dir_suffix)+1;
    string file_string = string(file);
    string file_dir_string = data_dir_string+file_string+"/";
    const char* file_dir = file_dir_string.c_str();
    // int length = strlen(data_dir)+strlen(file);
    // char file_dir [length];
    // strcpy(file_dir, data_dir);
    // strcat(file_dir, file);
    // strcat(file_dir, file_dir_suffix);

    // int order = 10;
    // while(dir_exists(file_dir)) {
    //     i += 1;
    //     if (i >= 100) {
    //         i = 0;
    //         std::cout <<
    //             "WARNING starting overwrite" <<
    //         std::endl;
    //         break;
    //     }
    //     if (i%order == 0) {
    //         if (i == order)
    //             length += 1;
    //         string mult_string = to_string(i/order);
    //         char mult = mult_string.c_str()[0];
    //         file_dir[length-2] = mult;
    //     }
    //
    //     string i_string = to_string(i%10);
    //     char i_char = i_string.c_str()[0];
    //     file_dir[length-1] = i_char;
    // }

    _mkdir(file_dir);

    string ext_string = ".txt";
    // const char* ext = ext_string.c_str();

    // const char* file_dir = const_cast<const char*>(file_dir);

    vector<string> file_strings;
    file_strings.push_back("vertices");
    file_strings.push_back("edges");
    file_strings.push_back("simplices");
    file_strings.push_back("pairs");
    // file_strings.push_back("stats");
    int nfiles = file_strings.size();

    // char* path;
    int path_length;
    for (int j = 0; j < nfiles; j++) {
        string file_name_string = "/"+file_strings[j]+ext_string;
        // const char* file_name = file_strings[j].c_str();
        const char* file_name = file_name_string.c_str();
        path_length = strlen(file_dir)+strlen(file_name);
        // char* path = new char [path_length]();
        char path [path_length];
        strcpy(path, file_dir);
        // strcat(path, "/");
        strcat(path, file_name);
        // strcat(path, ext);

        // // <editor-fold> PRINT WRITE
        // std::cout << "  -> writing to " << path <<
        // std::endl;
        // // </editor-fold> PRINT WRITE

        if (j == 0) write_vertices(path);
        else if (j == 1) write_edges(path);
        else if (j == 2) write_simplices(path);
        else if (j == 3) write_pairs(path);
        // else if (j == 4) write_stats(path);

        // if (j == 3) write_pairs(path);

        // delete [] path;
    }

    // string pair_string = "pair";
    // for (int j = 0; j < dim; j++) {
    //     string j_string = to_string(j);
    //     const char* j_char = j_string.c_str();
    //     const char* file_name = pair_string.c_str();
    //     path_length = strlen(file_dir)+strlen(j_char)+strlen(file_name)+strlen(ext)+1;
    //     path = new char [path_length];
    //     strcpy(path, file_dir);
    //     strcat(path, "/");
    //     strcat(path,j_char);
    //     strcat(path, file_name);
    //     strcat(path, ext);
    //
    //     double nsimplices = simplices.size();
    //
    //     ofstream myfile;
    //     myfile.open(path);
    //     for (int k = 0; k < pairs.get_num_pairs(); k++) {
    //         int birthi = pairs.get_pair(k).first;
    //         int deathi = pairs.get_pair(k).second;
    //         if (simplices[birthi]->dim == j){
    //             double birth = static_cast<double>(birthi)/nsimplices;
    //             double death = static_cast<double>(deathi)/nsimplices;
    //             if (death - birth > (j+2)/nsimplices)
    //                 myfile << birth << " " << death << "\n";
    //             // myfile << birth << " " << death << "\n";
    //         }
    //
    //     }
    //     myfile.close();
    //     // delete [] path;
    // }
    //
    string filt_pair_string = "pairs_filt";
    string file_name_string = "/"+filt_pair_string+ext_string;
    // const char* file_name = file_strings[j].c_str();
    const char* file_name = file_name_string.c_str();
    path_length = strlen(file_dir)+strlen(file_name);
    // char* path = new char [path_length]();
    char path [path_length];
    strcpy(path, file_dir);
    // strcat(path, "/");
    strcat(path, file_name);

    ofstream myfile;
    myfile.open(path);
    for (int k = 0; k < pairs.get_num_pairs(); k++) {
        int birthi = pairs.get_pair(k).first;
        int deathi = pairs.get_pair(k).second;
        double birth_filt = simplices[birthi]->filtration;
        double death_filt = simplices[deathi]->filtration;
        if (death_filt - birth_filt > 0.01)
            myfile << birth_filt << " " << death_filt << "\n";
    }
    myfile.close();

    // delete [] path;
}

void Graph::write_vertices(char* path) {
    ofstream myfile;
    myfile.open(path);
    for (int i = 0; i < vertices.size(); i++) {
        Vertex* v = vertices[i];
        // cout << "writing vertex " << v->index << endl;
        myfile <<
            "index(" << v->index << ")" << i_DELIM <<
            "point(" << v->point[0] << j_DELIM <<
                v->point[1] << j_DELIM << v->point[2] << ")\n";
    }
    myfile.close();
}

void Graph::write_edges(char* path) {
    ofstream myfile;
    myfile.open(path);
    for (int i = 0; i < edges.size(); i++) {
        Edge* e = edges[i];
        myfile <<
            "u(" << e->u->index << ")" << i_DELIM <<
            "v(" << e->v->index << ")" << i_DELIM <<
            "filtration(" << e->filtration << ")\n";
    }
    myfile.close();
}

void Graph::write_simplices(char* path) {
    ofstream myfile;
    myfile.open(path);
    for (int i = 0; i < simplices.size(); i++) {
        Simplex* s = simplices[i];
        myfile <<
            "index(" << s->index << ")" << i_DELIM <<
            "dim(" << s->dim << ")" << i_DELIM <<
            "faces(";
        int j = 0;
        set<int>::iterator it;
        for (it = s->faces.begin(); it != s->faces.end(); ++it) {
            myfile << (*it);
            if (j < s->faces.size()-1) myfile << j_DELIM;
            j += 1;
        }
        myfile << ")" << i_DELIM;

        myfile << "vertices(";
        j = 0;
        set<Vertex*>::iterator vt;
        for (vt = s->vertices.begin(); vt != s->vertices.end(); ++vt) {
            myfile << (*vt)->index;
            if (j < s->vertices.size()-1) myfile << j_DELIM;
            j += 1;
        }
        myfile << ")" << i_DELIM;

        myfile << "filtration(" << s->filtration << ")\n";
    }
    myfile.close();
}

void Graph::write_pairs(char* path) {
    ofstream myfile;
    myfile.open(path);
    for (int k = 0; k < pairs.get_num_pairs(); k++) {
        int birthi = pairs.get_pair(k).first;
        int deathi = pairs.get_pair(k).second;
        myfile << "birth(" << birthi << ")" << i_DELIM << "death(" << deathi << ")\n";
        // }

    }
    myfile.close();
}

// void Graph::write_boundary(char* path) {
//     ofstream myfile;
//     myfile.open(path);
//     for (int i = 0; i < simplices.size(); i++) {
//         Simplex* s = simplices[i];
//         myfile <<
//             "index(" << s->index << ")" << i_DELIM << "col(";
//         for (int i = 0; i < s->col.size(); i++) {
//             myfile << s->col[i];
//             if (i < simplices.size()-1) myfile << j_DELIM;
//         }
//         myfile << ")\n";
//     }
//     myfile.close();
// }

// void Graph::write_stats(char* path) {
//     ofstream myfile;
//     myfile.open(path);
//     int nvertices = vertices.size();
//     int nedges = edges.size();
//     double connectivity = static_cast<double>(nedges) /
//         static_cast<double>(nvertices+nedges);
//     myfile <<
//         "nvertices(" << nvertices << ")" << i_DELIM <<
//         "nedges(" << nedges << ")\n";
//
//     int nsimplices = simplices.size();
//     int kgt = nsimplices - nvertices - nedges;
//     double vert_ratio = static_cast<double>(nvertices)/static_cast<double>(nsimplices);
//     double edge_ratio = static_cast<double>(nedges)/static_cast<double>(nsimplices);
//     double kgt_ratio = static_cast<double>(kgt)/static_cast<double>(nsimplices);
//     myfile <<
//         "vratio(" << vert_ratio << ")" << i_DELIM <<
//         "eratio(" << edge_ratio << ")" << i_DELIM <<
//         "kratio(" << kgt_ratio << ")\n";
//
//     int npairs = pairs.get_num_pairs();
//     int nfeatures = features.size();
//     double noise = 1 - static_cast<double>(nfeatures)/static_cast<double>(npairs);
//     myfile <<
//         "npairs(" << npairs << ")" << i_DELIM <<
//         "nfeatures(" << nfeatures << ")" << i_DELIM <<
//         "noise(" << 100*kgt_ratio << ")\n";
//
//     myfile.close();
// }

// </editor-fold> write


#endif /* graph_h */
