#include "C_func_file.h"

int multiply_by_10_in_C(double arr[][], unsigned int m, unsigned int n,int point[])
{
    unsigned int i, j;
    int sum = 0;
    for (i = 0; i < m; i++) {
        for (i=0; j < n; j++)
            arr[i][j] *= 10;
            sum = sum + arr[i][j];
    }
    point[0] = 200;
    point[1] = 34;
    return sum;
}