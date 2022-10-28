#ifndef LIVEWIRE_H
#define LIVEWIRE_H

#include <vector>
#include <cmath>
struct SEntry {
	short    sX;         // X-coordinate
	short    sY;         // Y-coordinate
	long     lLinInd;    // Linear index from x and y for 1D-array
	float    flG;        // The current cost from seed to (X,Y)^T
};
inline long ifMin(long a, long b)
{
	return a < b ? a : b;
}

inline long ifMax(long a, long b)
{
	return a > b ? a : b;
}


inline long ifLinInd(short sX, short sY, short sNX)
{
	//    return long(sX)*long(sNY) + long(sY);
	return long(sY)*long(sNX) + long(sX);
}

long fFindMinG(SEntry *pSList, long lLength) {
	long    lMinPos = 0;
	float   flMin = 1e15;
	SEntry  SE;
	for (long lI = 0; lI < lLength; lI++) {
		SE = *pSList++;
		if (SE.flG < flMin) {
			lMinPos = lI;
			flMin = SE.flG;
		}
	}
	return lMinPos;
}

long fFindLinInd(SEntry *pSList, long lLength, long lInd)
{
	SEntry SE;

	for (long lI = 0; lI < lLength; lI++) {
		SE = *pSList++;
		if (SE.lLinInd == lInd) return lI;
	}
	return -1; // If not found, return -1
}

void calcIdealAnchor(double imgf[], unsigned int rows, unsigned int cols, int point[], int rad);
void calcLiveWireP(double imgS[], unsigned int rows, unsigned int cols, int point[], int iPX[], int iPY[], int lE[], double dRadius, int LISTMAXLENGTH);
int calcLiveWireGetPath(int ipx[], unsigned int rows, unsigned int cols, int ipy[], int pxy[], int pathx[], int pathy[], int iMAXPATH);
void calcLWP(int point[], double imgf[],  unsigned int rows, unsigned int cols);
int calcLWPath(int p[], double imgf[], unsigned int rows, unsigned int cols, int ipx[], int ipy[], int pathx[], int pathy[], int cPoint[]);


#endif