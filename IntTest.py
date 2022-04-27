#---------------------------------------
#
#
#		 _______	mtr			mtr		cn		wire
#		/		\	blue		1		1		2B
#		|		|	pink		2		2		1A
#		| motor	|	red			3		nc		
#		|		|	orange		4		4		2A
#		\______/	yellow		5		3		1B
#
#												sig
#		vcc										rst
#		#0										slp
#		#26										stp
#		#25										dir
#
#import machine
from machine import Pin
import time
import DaikeiSeigyo
#from DaikeiSeigyo import DaikeiSeigyo

#---------------------------------------
#
g_nIndex	: int	# 0 <= idx < 800
g_nPulseCnt	: int
g_nThinCnt	: int	# 0 <= cnt
g_bOnOff	: bool	# 0 or 1
g_list = []

#---------------------------------------
#
LED_PIN		= 10
STEP_PIN	= 26
DIR_PIN		= 25
SLP_PIN		= 0
BTN_A_PIN	= 37
BTN_B_PIN	= 39

#---------------------------------------
#
led		= Pin(LED_PIN, Pin.OUT)
stp		= Pin(STEP_PIN, Pin.OUT)
dir		= Pin(DIR_PIN, Pin.OUT)
slp		= Pin(SLP_PIN, Pin.OUT, value=False)
btn_a	= Pin(BTN_A_PIN, mode=Pin.IN, pull=Pin.PULL_UP)
btn_b	= Pin(BTN_B_PIN, mode=Pin.IN, pull=Pin.PULL_UP)

#---------------------------------------
#
#def mycallback(t):
def mycallback():
	global	g_nIndex
	global	g_nThinCnt
	global	g_nPulseCnt
	global	g_bOnOff

	if (g_nIndex < g_nPulseCnt):

#		print(g_nIndex, g_nThinCnt, g_bOnOff)

		if (g_nThinCnt > 0):
			g_nThinCnt -= 1

		else:
			if (g_bOnOff):
				g_nThinCnt = g_list[g_nIndex][1] - 1
				g_bOnOff = False;

			else:
				g_nThinCnt = g_list[g_nIndex][0] - 1
				g_nIndex += 1
				g_bOnOff = True;

		led.value(g_bOnOff)
		stp.value(g_bOnOff)


#---------------------------------------
#
_MAX_PPS	=	500
_START_PPS	=	100
_ACC_PPS	=	500
_RED_PPS	=	-_ACC_PPS
_MAX_EXAM	=	500

g_list = DaikeiSeigyo.GetDaikeiList(_MAX_EXAM, _START_PPS, _MAX_PPS, _ACC_PPS, _RED_PPS)

while (True):
	if btn_b.value() == 0:
		break

	if btn_a.value() == 0:

		g_nIndex	= int(0)
		g_nPulseCnt	= len(g_list)
		print(g_nPulseCnt)
		g_nThinCnt	= g_list[g_nIndex][0] - 1
		g_bOnOff	= True

		slp.value(True)			# sleep out
		time.sleep_ms(100)

		while (g_nIndex < g_nPulseCnt):
			mycallback()
			time.sleep_us(10)

		time.sleep_ms(100)
		slp.value(False)		# sleep in

	if btn_a.value() == 0:
		pass

#t0 = machine.Timer(0)
#t0.init(mode = machine.Timer.PERIODIC, period = 1, callback = mycallback)
