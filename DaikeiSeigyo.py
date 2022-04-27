#-------------------------------------------------------------------------------
#
#	https://abundcore.net/archives/1449
#	https://micropython-docs-ja.readthedocs.io/ja/latest/library/machine.Timer.html
#	https://micropython-docs-ja.readthedocs.io/ja/latest/esp32/quickref.html
#

#---------------------------------------
#
#
import math

#---------------------------------------
#
#
_MAX_PPS	=	500
_START_PPS	=	100
_ACC_PPS	=	500
_RED_PPS	=	-_ACC_PPS
#_INT_FREQ	=	100000		# Hz
_INT_FREQ	=	10000		# Hz
_MAX_EXAM	=	500

#---------------------------------------
#
_PRINT_CSV		=	0
_MAKE_LIST		=	1
_PRINT_INFO		=	1

#---------------------------------------
# globals
#
g_nSumPulseWidth : int = 0
g_lstItems = []
g_nItems : int = 0
#---------------------------------------
#
#
def CalcPulseSub(nPulseIdx : int, nMaxPps : int, nStartPps : int, nAccPps : int, nIntFreq : int):

	global g_nSumPulseWidth
	global g_nItems

	fIdealPulse		: float
	nPulseWidth		: int
	nOnPulseWidth	: int
	nOffPulseWidth	: int
	fTime			: float
	fTruePulse		: float

	# 理想パルス
	#
	fIdealPulse = math.sqrt(nStartPps ** 2 + 2 * nAccPps * nPulseIdx)
	if (fIdealPulse > nMaxPps):
		fIdealPulse = nMaxPps

	# パルス幅
	#
	nPulseWidth = nIntFreq / fIdealPulse

	# オン・オフ　パルス幅
	#
	nOnPulseWidth = int(nPulseWidth / 2)
	nOffPulseWidth = int(nPulseWidth - nOnPulseWidth)

	# 経過時間
	#
	g_nSumPulseWidth += nPulseWidth
	fTime = g_nSumPulseWidth / nIntFreq

	# 実パルス速度
	fTruePulse = nIntFreq / nPulseWidth

	if (_PRINT_CSV):
		print("{", '{:.3f}'.format(nOnPulseWidth), ",", '{:.3f}'.format(nOffPulseWidth), "},")

	elif (_MAKE_LIST):
		item = [nOnPulseWidth, nOffPulseWidth]
		g_lstItems.append(item)

	elif (_PRINT_INFO):
		print(nPulseIdx, ",",					\
		'{:.3f}'.format(fIdealPulse), ",",		\
		'{:.3f}'.format(nOnPulseWidth), ",",	\
		'{:.3f}'.format(nOffPulseWidth), ",",	\
		'{:.3f}'.format(nPulseWidth), ",",		\
		'{:.3f}'.format(fTime), ",",			\
		'{:.3f}'.format(fTruePulse))

	g_nItems += 1

#---------------------------------------
#
#
def CalcPulseWidth(nMaxPps : int, nStartPps : int, nAccPps : int, nIntFreq : int, nStartPulse : int, nEndPulse : int, nIncPulse : int):

	assert type(nEndPulse) == int

#	print(type(nStartPulse))
#	print(type(nEndPulse))
#	print(type(nIncPulse))



	# 加速 or 平常
	#
	if (nIncPulse >= 0):
		for i in range (nStartPulse, nEndPulse, nIncPulse):
			CalcPulseSub(i, nMaxPps, nStartPps, nAccPps, nIntFreq)

	# 減速
	#
	else:
		for i in range (nStartPulse, nEndPulse, nIncPulse):
			CalcPulseSub(i, nMaxPps, nStartPps, nAccPps, nIntFreq)

#---------------------------------------
#
#
def GetDaikeiList(total_pulse, start_pps, max_pps, acc_pps, red_pps):

	global g_nSumPulseWidth
	global g_nItems

	g_nSumPulseWidth = 0
	g_lstItems.clear()
	g_nItems = 0

	nAccPulse : int			= (max_pps ** 2 - start_pps ** 2) / 2 / acc_pps
	nNormalPulse : int		= total_pulse - nAccPulse - nAccPulse
	nRedPulse : int			= total_pulse - nAccPulse - nNormalPulse

	if (_PRINT_INFO):
		print("acc pulse = ", nAccPulse, "norm pulse = ", nNormalPulse, "red pulse = ", nRedPulse)

	CalcPulseWidth(max_pps, start_pps, acc_pps, _INT_FREQ, int(0), int(nAccPulse), 1)
	CalcPulseWidth(max_pps, start_pps, acc_pps, _INT_FREQ, int(nAccPulse), int(nAccPulse + nNormalPulse), 1)
	CalcPulseWidth(max_pps, start_pps, acc_pps, _INT_FREQ, int(nRedPulse), 0, -1)

#	if (_MAKE_LIST):
#		print(g_lstItems)
#		print(len(g_lstItems))

	return g_lstItems

if __name__ == "__main__":
	GetDaikeiList(_MAX_EXAM, _START_PPS, _MAX_PPS, _ACC_PPS, _RED_PPS)
