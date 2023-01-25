#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include "./grower.h"

#define ROWS 3000
#define COLS 3000
#define GEN 5000

// 2D array for the current state of the cells
int current[ROWS+2][COLS+2];
// 2D array for the next state of the cells
int next[ROWS+2][COLS+2];

// function to initialize the cells
void init() {
    int i, j;
    int height = GROWER_HEIGHT, width = GROWER_WIDTH;

    for (i = 0; i < ROWS+2; i++) {
        for (j = 0; j < COLS+2; j++) {
            current[i][j] = 0;
            next[i][j] = 0;

        }
    }
    for (i = 0; i < height; i++) {
        for (j = 0; j < width; j++) {
            current[ROWS/2+i][COLS/2+j] = grower[i][j];
        }
    }
}


// function to calculate the next state of the cells
void step() {
    int i, j;
    #pragma omp parallel for collapse(2) private(i,j)
    for (i = 1; i <= ROWS; i++) {
        for (j = 1; j <= COLS; j++) {
            // count the number of alive neighbors
            int alive = 0;
            if (current[i-1][j-1]) { alive++; }
            if (current[i-1][j]) { alive++; }
            if (current[i-1][j+1]) { alive++; }
            if (current[i][j-1]) { alive++; }
            if (current[i][j+1]) { alive++; }
            if (current[i+1][j-1]) { alive++; }
            if (current[i+1][j]) { alive++; }
            if (current[i+1][j+1]) { alive++; }

            // apply the rules of the Game of Life
            if (current[i][j]) {
                // cell is alive
                if (alive < 2 || alive > 3) {
                    next[i][j] = 0;
                } else {
                    next[i][j] = 1;
                }
            } else {
                // cell is dead
                if (alive == 3) {
                    next[i][j] = 1;
                } else {
                    next[i][j] = 0;
                }
            }
        }
    }

    // copy the next state to the current state
    #pragma omp parallel for collapse(2) private(i,j)
    for (i = 1; i <= ROWS; i++) {
        for (j = 1; j <= COLS; j++) {
            current[i][j] = next[i][j];
        }
    }
}

int main() {
    // initialize the cells
    init();

    // iterate the Game of Life for 100 steps
    int i, j;
    int res = 0;
    for (i = 0; i < GEN; i++) {
        step();
    }
    for (i = 1; i <= ROWS; i++) {
        for (j = 1; j <= COLS; j++) {
            if(current[i][j] > 0) {
                res++;
            } 
        }
    }
    printf("%d ", res);
    return 0;
}