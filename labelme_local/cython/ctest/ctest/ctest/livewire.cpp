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
	int*   plE = lE;// ���ڼ���ĳ�����Ƿ񱻴������׼ȷ��˵��ĳ������ֵ
	SEntry *pSList = new SEntry[LISTMAXLENGTH];
	lNPixelsToProcess = ifMin(long(3.14*dRadius*dRadius + 0.5), long(sNX)*long(sNY)); // �趨��һ��������Χ����Ȼȫͼ����̫����

	// Initialize active list with zero cost seed pixel.
	SQ.sX = sXSeed;
	SQ.sY = sYSeed;
	//    SQ.lLinInd  = ifLinInd(sXSeed, sYSeed, sNY);
	SQ.lLinInd = ifLinInd(sXSeed, sYSeed, sNX); // ��֪��ԭ���Ǹ�ָ������index
	SQ.flG = 0.0; // ����cost
	pSList[lListInd++] = SQ;  // �ú�ӣ�Ҳ������pSList[0] = SQ, Ȼ��lListInd++

	// While there are still objects in the active list and pixel limit not reached
	while ((lListInd) && (lNPixelsProcessed < lNPixelsToProcess)) { //�����Գ�ʼ���ӵ�Ϊ���Ķ�̬�滮���԰뾶ΪdRadius��Բ����ڸ�λ�õ����·����
		// ����iPX��iPY�������·������������ �������ӵ㵽���Ͻǣ������Ͻǵ�iPXΪ1��iPYΪ1��Ҳ����˵�Ӹõ�����½ǵ�λ�ù�����·������̵�
		// ----------------------------------------------------------------
		// Determine pixel q in list with minimal cost and remove from
		// active list. Mark q as processed.
		lInd = fFindMinG(pSList, lListInd); // �ҳ�pSList��costֵ��С��λ��
		SQ = pSList[lInd];
		lListInd--;
		pSList[lInd] = pSList[lListInd]; // �����һ��Ԫ�ظ���pSList��costֵ��С��λ�ã� ��������ֻ�е��һ�βŻ����
		plE[SQ.lLinInd] = 1; // ��ʾ��һ��ֵ�Ѿ��������
		// ----------------------------------------------------------------
		// Determine neighbourhood of q and loop over it 3*3�Ĵ���
		sXLowerLim = ifMax(0, SQ.sX - 1);
		sXUpperLim = ifMin(sNX - 1, SQ.sX + 1);
		sYLowerLim = ifMax(0, SQ.sY - 1);
		sYUpperLim = ifMin(sNY - 1, SQ.sY + 1);
		for (short sX = sXLowerLim; sX <= sXUpperLim; sX++) {
			for (short sY = sYLowerLim; sY <= sYUpperLim; sY++) {
				// - - - - - - - - - - - - - - - - - - - - - - - - - - - -
				// Skip if pixel was already processed
				//                lLinInd = ifLinInd(sX, sY, sNY);
				lLinInd = ifLinInd(sX, sY, sNX);  // ֻ�Ǽ򵥵ؼ���ָ�������ֵ
				if (plE[lLinInd]) continue; // plE��һ����ͼ��ͬ����С�ı�־λ�������ĳ������λ����1�˱�����һ��λ���Ѿ����������
				// - - - - - - - - - - - - - - - - - - - - - - - - - - - -
				// Compute the new accumulated cost to the neighbour pixel
				if ((abs(sX - SQ.sX) + abs(sY - SQ.sY)) == 1) flWeight = 0.71; else flWeight = 1; // �Խ��ߵ�����Ȩֵ����һ�������������sqrt(2)������
				flThisG = SQ.flG + float(pdF[lLinInd])*flWeight; // ԭ��pdf��cost����Ȼ��lLinInd��ָ��������
				// - - - - - - - - - - - - - - - - - - - - - - - - - - - -
				// Check whether r is already in active list and if the
				// current cost is lower than the previous
				lInd = fFindLinInd(pSList, lListInd, lLinInd); // ����pSList�����iLinInd������pSList�򷵻�1�����򷵻�-1
				if (lInd >= 0) {  // �����pSList�ˣ�����ȡ�������£���û�ж�����
					SR = pSList[lInd];
					if (flThisG < SR.flG) {
						SR.flG = flThisG;
						pSList[lInd] = SR;
						plPX[lLinInd] = int(SQ.sX - sX);
						plPY[lLinInd] = int(SQ.sY - sY); // ����Ӧ���Ǽ�¼ĳ������λ�õ���������
					}
				}
				else { // �������
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
	while ((ipx[iYS*cols + iXS] != 0) || (ipy[iYS*cols + iXS] != 0)) // We're not at the seed�����ipx����ipy��ֵ��ʾ�õ���������ӵ������·��
	{
		iXS = iXS + ipx[iYS*cols + iXS];
		iYS = iYS + ipy[iYS*cols + iXS]; // ��ʼ����ֱ�����ӵ㣬�����������pxy���Ѿ�������parRadiusR����ô�޷������ѭ��
		iLength = iLength + 1;
		iX[iLength] = iXS;
		iY[iLength] = iYS;
	}
	int count = 0;
	for (int ii = iLength - 2; ii >= 0; ii--) { // ��������������㣬��ôֱ�ӷ��ؿ�
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
	double pDST = sqrt(pow((p[0] -cPoint[0]), 2) + pow((p[1] - cPoint[1]), 2)); // cPoint�ǳ�ʼ���ӵ�
	bool isNoPath = true;
	int parRadiusPath = 300;
	int num = 0;
	if ((pDST > 1.0) && (pDST < parRadiusPath)) { // ��������˾ֲ���̬�滮��Χ����ôֱ�ӷ���һ���㣬����������ֱ�ߣ�����Ϊɶ��parRadiusR��һ����
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