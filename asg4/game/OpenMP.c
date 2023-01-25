#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include "./grower.h"

#define ROWS 3000
#define COLS 3000
#define GEN 5000

// the current state of the cells
int current[ROWS+2][COLS+2];
// the next state of the cells
int next[ROWS+2][COLS+2];

// function to initialize the cells
void init() {
    int i, j;
    if (!GROWER_HEIGHT || !GROWER_WIDTH) {
        fprintf(stderr, "GROWER_HEIGHT or GROWER_WIDTH is unvalid\n");
        exit(EXIT_FAILURE);
    }

    if (grower == NULL || !sizeof(grower[0]) || !sizeof(grower[0][0])) {
        fprintf(stderr, "grower is unvalid\n");
        exit(EXIT_FAILURE);
    }

    int rows_num = sizeof(grower)/sizeof(grower[0]), cols_num = sizeof(grower[0])/sizeof(grower[0][0]);
    if (GROWER_HEIGHT != rows_num || GROWER_WIDTH != cols_num) {
        fprintf(stderr, "grower's rows_num/cols_num don't match GROWER_HEIGHT/GROWER_WIDTH \n");
        exit(EXIT_FAILURE);
    }

    if (GROWER_HEIGHT > ROWS/2 || GROWER_WIDTH > COLS/2) {
        fprintf(stderr, "grower's length is bigger than the size of current state\n");
        exit(EXIT_FAILURE);
    }

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


// calculate the next state of the cells
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
    init();
    int i, j;
    int res = 0;

    // iterate the Game of Life
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