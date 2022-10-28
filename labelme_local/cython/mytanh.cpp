#include <cmath>

const double e = 2.7182818284590452353602874713527;

double mysinh(double x)
{
    return (1 - pow(e, (-2 * x))) / (2 * pow(e, -x));
}

double mycosh(double x)
{
    return (1 + pow(e, (-2 * x))) / (2 * pow(e, -x));
}

double mytanh(double x)
{
    return mysinh(x) / mycosh(x);
}
