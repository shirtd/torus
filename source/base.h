//
//  base.h
//  tdsp
//
//  Created by kirk gardner on 4/11/17.
//  Copyright © 2017 kirk gardner. All rights reserved.
//

#ifndef base_h
#define base_h

#include <iostream>
#include <fstream>
#include <stdio.h>
#include <string.h>
#include <cstring>
#include <sys/stat.h>

#include <sstream>
#include <iomanip>

#include <mutex>
#include <thread>

//#include <complex.h>
//#include <fftw3.h>
//#include <sndfile.h>
#include <math.h>

#include "point.h"

// wrapper algorithm that computes the persistence pairs of a given boundary matrix using a specified algorithm
#include <phat/compute_persistence_pairs.h>

// main data structure (choice affects performance)
#include <phat/representations/vector_vector.h>

// algorithm (choice affects performance)
#include <phat/algorithms/standard_reduction.h>
#include <phat/algorithms/chunk_reduction.h>
#include <phat/algorithms/row_reduction.h>
#include <phat/algorithms/twist_reduction.h>

using namespace std;
using namespace phat;

// // #define BLOCK_SIZE 1024
// #define BLOCK_SIZE 4096
// // #define BLOCK_SIZE 8192
// #define RATE 44100
// #define MAX_CHANNELS 6
// #define MIN_HZ 20
// #define MAX_HZ 20000
// #define PCS 12
// #define BPM 113
// #define PHRASE 8
// #define SCALE 1
#define PERS_THRESH 0
// #define PCS_THRESH 0.024

// TODO
// #define i_DELIM "\n"
// #define j_DELIM "\t"
// #define k_DELIM ","
// // #define l_DELIM " "

#define i_DELIM "\t"
#define j_DELIM ","
#define k_DELIM " "

struct stat sb;

// static std::string notes [12] = {
//
//     "A",
//     "A#/Bb",
//     "B",
//     "C",
//     "C#/Db",
//     "D",
//     "D#/Eb",
//     "E",
//     "F",
//     "F#/Gb",
//     "G",
//     "G#/Ab"
//
// };

// struct SF {
//     SF_INFO info;
//     SNDFILE* pointer;
// };

// struct pc {
//     int i;
//     double v;
//
//     bool operator<( const pc& rhs) const { return v < rhs.v; }
// };
//
// class pcsample_t {
// public:
//     double* sample;
//     pc* sorted;
//
//     double max;
//     int maxi;
//     double sum;
//
//     pcsample_t();
//     pcsample_t(double* s);
//
// private:
//
//     void maxpcs();
//     void sortpcs();
//
// };
//
// pcsample_t::pcsample_t() {
//     sorted = new pc [PCS];
//     sample = new double [PCS];
//     max = 0;
//     maxi = -1;
//     sum = 0;
// }
//
// pcsample_t::pcsample_t(double* s) {
//     sorted = new pc [PCS];
//     sample = s;
//     max = 0;
//     maxi = -1;
//     sum = 0;
//
//     maxpcs();
//     sortpcs();
// }
//
// void pcsample_t::maxpcs() {
//     for (int i = 0; i < PCS; i++) {
//         sum += sample[i];
//         if (sample[i] > max) {
//             max = sample[i];
//             maxi = i;
//         }
//     }
// }
//
// void pcsample_t::sortpcs() {
//     for (int i = 0; i < PCS; i++) {
//         sorted[i].i = i;
//         sorted[i].v = sample[i];
//     }
//     std::sort(sorted,sorted+12);
// }
//
//
// static int btop(int bin) {
//     double f = (bin)*RATE/BLOCK_SIZE;
//     double pc_d = 12*log2(f/440) + 48;
//     int pc = round(pc_d);
//     if ((pc < 0) && (bin != 0))
//         std::cout << "bin " << bin << " -> pc " << pc << std::endl;
//     return pc;
// }
//
// static int ftob(double f) {
//    return round(f*BLOCK_SIZE/RATE);
// }
//
// static double magnitude(double x, double y) {
//     return sqrt(x*x + y*y);
// }
//
// static double TIME(int n) {
//     return static_cast<double>(n*BLOCK_SIZE)/RATE;
// }
//
// static double dist(Point<double> u, Point<double> v) {
//     return sqrt((u[0]-v[0])*(u[0]-v[0]) + (u[1]-v[1])*(u[1]-v[1]));
// }

double dist3(Point<double,3> u, Point<double,3> v) {
    return sqrt((u[0]-v[0])*(u[0]-v[0]) + (u[1]-v[1])*(u[1]-v[1]) + (u[2] - v[2])*(u[2] - v[2]));
}

// static bool same_phrase(double s, double t) {
//     return (abs(s - t) < PHRASE*60/BPM);
// }

bool _mkdir(const char* dir) {
    const int dir_err = mkdir(dir, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
    if (dir_err == -1) {
        std::cout << " ! error creating directory " << dir << std::endl;
        return false;
    } else {
        // std::cout << "\t > created directory " << dir << std::endl;
        return true;
    }
}

bool dir_exists(const char* dir) {
    if (stat(dir, &sb) == 0 && S_ISDIR(sb.st_mode)) {
        // std::cout << "directory " << dir << " exists " << std::endl;
        return true;
    } return false;
}

string to_string_double(double a_value, const int n = 4) {
    std::ostringstream out;
    // out << std::setprecision(n) << a_value;
    out << a_value;
    return out.str();
}

#endif /* base_h */
