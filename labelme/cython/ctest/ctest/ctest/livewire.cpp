#include "livewire.h"

void calcIdealAnchor(double imgf[], unsigned int rows, unsigned int cols, int point[], int rad) {
	int nc = cols;
	int nr = rows;
	int r0 = point[1];
	int c0 = point[0];

	int rMin = r0 - rad;
	int rMax = r0 + rad;
	if (rMin < 0) {
		rMin = 0;
	}
	if (rMax >= nr) {
		rMax = nr - 1;
	}

	int cMin = c0 - rad;
	int cMax = c0 + rad;
	if (cMin < 0) {
		cMin = 0;
	}
	if (cMax >= nc) {
		cMax = nc - 1;
	}
	double valMin = imgf[r0*nr + c0];
	double tval;
	for (int rr = rMin; rr < rMax; rr++) {
		for (int cc = cMin; cc < cMax; cc++) {
			tval = imgf[rr*nr + cc];
			if (tval < valMin) {
				valMin = tval;
				point[0] = cc;
				point[1] = rr;
			}
		}
	}
}

void calcLiveWireP(double imgS[], unsigned int rows, unsigned int cols, int point[], int iPX[], int iPY[], int lE[], double dRadius, int LISTMAXLENGTH) {
	double *pdF = imgS;
	short   sNX = cols;
	short   sNY = rows;
	short   sXSeed = point[0];
	short   sYSeed = point[1];
	int *plPX = iPX;
	int *plPY = iPY;

	// Start of the real functionality
	long    lInd;
	long    lLinInd;
	long    lListInd = 0; // = length of list
	short   sXLowerLim;
	short   sXUpperLim;
	short   sYLowerLim;
	short   sYUpperLim;
	long    lNPixelsToProcess;
	long    lNPixelsProcessed = 0;

	float   flThisG;
	float   flWeight;

	SEntry  SQ, SR; 
	int*   plE = lE;// 用于记载某个点是否被处理过，准确来说是某个索引值
	SEntry *pSList = new SEntry[LISTMAXLENGTH];
	lNPixelsToProcess = ifMin(long(3.14*dRadius*dRadius + 0.5), long(sNX)*long(sNY)); // 设定了一个搜索范围，不然全图搜索太大了

	// Initialize active list with zero cost seed pixel.
	SQ.sX = sXSeed;
	SQ.sY = sYSeed;
	//    SQ.lLinInd  = ifLinInd(sXSeed, sYSeed, sNY);
	SQ.lLinInd = ifLinInd(sXSeed, sYSeed, sNX); // 不知道原来是个指针索引index
	SQ.flG = 0.0; // 储存cost
	pSList[lListInd++] = SQ;  // 用后加，也就是先pSList[0] = SQ, 然后lListInd++

	// While there are still objects in the active list and pixel limit not reached
	while ((lListInd) && (lNPixelsProcessed < lNPixelsToProcess)) { //这是以初始种子点为中心动态规划到以半径为dRadius的圆面积内各位置的最短路径，
		// 其中iPX和iPY储存最短路径的索引方向， 比如种子点到左上角，那左上角的iPX为1，iPY为1，也就是说从该点的右下角的位置过来的路径是最短的
		// ----------------------------------------------------------------
		// Determine pixel q in list with minimal cost and remove from
		// active list. Mark q as processed.
		lInd = fFindMinG(pSList, lListInd); // 找出pSList中cost值最小的位置
		SQ = pSList[lInd];
		lListInd--;
		pSList[lInd] = pSList[lListInd]; // 将最后一个元素赋给pSList中cost值最小的位置， 可是这里只有点击一次才会调用
		plE[SQ.lLinInd] = 1; // 表示这一个值已经处理过了
		// ----------------------------------------------------------------
		// Determine neighbourhood of q and loop over it 3*3的窗口
		sXLowerLim = ifMax(0, SQ.sX - 1);
		sXUpperLim = ifMin(sNX - 1, SQ.sX + 1);
		sYLowerLim = ifMax(0, SQ.sY - 1);
		sYUpperLim = ifMin(sNY - 1, SQ.sY + 1);
		for (short sX = sXLowerLim; sX <= sXUpperLim; sX++) {
			for (short sY = sYLowerLim; sY <= sYUpperLim; sY++) {
				// - - - - - - - - - - - - - - - - - - - - - - - - - - - -
				// Skip if pixel was already processed
				//                lLinInd = ifLinInd(sX, sY, sNY);
				lLinInd = ifLinInd(sX, sY, sNX);  // 只是简单地计算指针的索引值
				if (plE[lLinInd]) continue; // plE是一个与图像同样大小的标志位矩阵，如果某个像素位置置1了表明这一个位置已经被处理过了
				// - - - - - - - - - - - - - - - - - - - - - - - - - - - -
				// Compute the new accumulated cost to the neighbour pixel
				if ((abs(sX - SQ.sX) + abs(sY - SQ.sY)) == 1) flWeight = 0.71; else flWeight = 1; // 对角线的邻域权值更大一丢丢，具体就是sqrt(2)的问题
				flThisG = SQ.flG + float(pdF[lLinInd])*flWeight; // 原来pdf是cost矩阵，然后lLinInd是指针索引号
				// - - - - - - - - - - - - - - - - - - - - - - - - - - - -
				// Check whether r is already in active list and if the
				// current cost is lower than the previous
				lInd = fFindLinInd(pSList, lListInd, lLinInd); // 遍历pSList，如果iLinInd存在于pSList则返回1，否则返回-1
				if (lInd >= 0) {  // 如果在pSList了，则将它取出来更新（并没有丢掉）
					SR = pSList[lInd];
					if (flThisG < SR.flG) {
						SR.flG = flThisG;
						pSList[lInd] = SR;
						plPX[lLinInd] = int(SQ.sX - sX);
						plPY[lLinInd] = int(SQ.sY - sY); // 这里应该是记录某个像素位置的索引方向
					}
				}
				else { // 否则加入
				 // - - - - - - - - - - - - - - - - - - - - - - - - - -
				 // If r is not in the active list, add it!
					SR.sX = sX;
					SR.sY = sY;
					SR.lLinInd = lLinInd;
					SR.flG = flThisG;
					pSList[lListInd++] = SR;
					plPX[lLinInd] = int(SQ.sX - sX);
					plPY[lLinInd] = int(SQ.sY - sY);
					// - - - - - - - - - - - - - - - - - - - - - - - - - -
				}
			}
			// End of the neighbourhood loop.
			// ----------------------------------------------------------------
		}
		lNPixelsProcessed++;
	}
	// End of while loop
	delete pSList;
}

int calcLiveWireGetPath(int ipx[], unsigned int rows, unsigned int cols, int ipy[], int pxy[], int pathx[], int pathy[], int iMAXPATH)
{
	//path.clear();
	// Initialize the variables
	int iXS = pxy[0];
	int iYS = pxy[1];
	std::vector<int> iX(iMAXPATH, 0);
	std::vector<int> iY(iMAXPATH, 0);
	int iLength = 0;
	iX[iLength] = iXS;
	iY[iLength] = iYS;
	while ((ipx[iYS*cols + iXS] != 0) || (ipy[iYS*cols + iXS] != 0)) // We're not at the seed，如果ipx或者ipy有值表示该点具有离种子点最近的路径
	{
		iXS = iXS + ipx[iYS*cols + iXS];
		iYS = iYS + ipy[iYS*cols + iXS]; // 开始逆推直到种子点，但是如果本身pxy就已经超出了parRadiusR，那么无法进入该循环
		iLength = iLength + 1;
		iX[iLength] = iXS;
		iY[iLength] = iYS;
	}
	int count = 0;
	for (int ii = iLength - 2; ii >= 0; ii--) { // 如果不超过两个点，那么直接返回空
		int tx = iX[ii];
		int ty = iY[ii];
		pathx[count] = tx;
		pathy[count] = ty;
		count += 1;
	}
	return count - 1;
}

void calcLWP(int point[], double imgf[], unsigned int rows, unsigned int cols) {
	calcIdealAnchor(imgf, rows, cols, point, 4);
}

int calcLWPath(int p[], double imgf[], unsigned int rows, unsigned int cols, int ipx[], int ipy[], int pathx[], int pathy[], int cPoint[]) {
	calcIdealAnchor(imgf, rows, cols, p, 4);
	double pDST = sqrt(pow((p[0] -cPoint[0]), 2) + pow((p[1] - cPoint[1]), 2)); // cPoint是初始种子点
	bool isNoPath = true;
	int parRadiusPath = 300;
	int num = 0;
	if ((pDST > 1.0) && (pDST < parRadiusPath)) { // 如果超出了局部动态规划范围，那么直接返回一个点，让他们连成直线，可是为啥和parRadiusR不一样？
		num = calcLiveWireGetPath(ipx, rows, cols,ipy, p, pathx, pathy, 1000);
		if (num > 0) {
			isNoPath = false;
		}
	}
	if (isNoPath) {
		num = 1;
		pathx[0] = p[0];
		pathy[0] = p[1];
	}
	return num;

}