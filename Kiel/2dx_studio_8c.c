//2DX3 Final Project
//Code Written by: Areeb Jamal
//Student Number: 400315588
//Macid: jamala19

//Given and required
#include <stdint.h>
#include "tm4c1294ncpdt.h"
#include "vl53l1x_api.h"
#include "PLL.h"
#include "SysTick.h"
#include "uart.h"
#include "onboardLEDs.h"
#include <math.h>

#define I2C_MCS_ACK             0x00000008  // Data Acknowledge Enable
#define I2C_MCS_DATACK          0x00000008  // Acknowledge Data
#define I2C_MCS_ADRACK          0x00000004  // Acknowledge Address
#define I2C_MCS_STOP            0x00000004  // Generate STOP
#define I2C_MCS_START           0x00000002  // Generate START
#define I2C_MCS_ERROR           0x00000002  // Error
#define I2C_MCS_RUN             0x00000001  // I2C Master Enable
#define I2C_MCS_BUSY            0x00000001  // I2C Busy
#define I2C_MCR_MFE             0x00000010  // I2C Master Function Enable
#define MAXRETRIES              5           // number of receive attempts before giving up

//Given code
//---- Pin Allocation and Setup ----
void I2C_Init(void){
  SYSCTL_RCGCI2C_R |= SYSCTL_RCGCI2C_R0;           													// activate I2C0
  SYSCTL_RCGCGPIO_R |= SYSCTL_RCGCGPIO_R1;          												// activate port B
  while((SYSCTL_PRGPIO_R&0x0002) == 0){};																		// ready?

    GPIO_PORTB_AFSEL_R |= 0x0C;           																	// 3) enable alt funct on PB2,3       0b00001100
    GPIO_PORTB_ODR_R |= 0x08;             																	// 4) enable open drain on PB3 only

    GPIO_PORTB_DEN_R |= 0x0C;             																	// 5) enable digital I/O on PB2,3
//    GPIO_PORTB_AMSEL_R &= ~0x0C;          																// 7) disable analog functionality on PB2,3

                                                                            // 6) configure PB2,3 as I2C
//  GPIO_PORTB_PCTL_R = (GPIO_PORTB_PCTL_R&0xFFFF00FF)+0x00003300;
  GPIO_PORTB_PCTL_R = (GPIO_PORTB_PCTL_R&0xFFFF00FF)+0x00002200;    //TED
    I2C0_MCR_R = I2C_MCR_MFE;                      													// 9) master function enable
    I2C0_MTPR_R = 0b0000000000000101000000000111011;                       	// 8) configure for 100 kbps clock (added 8 clocks of glitch suppression ~50ns)
//    I2C0_MTPR_R = 0x3B;                                        						// 8) configure for 100 kbps clock
        
}

//Use port G (PG0) to reset VL53LIX using XSHUT
void PortG_Init(void){
    //Use PortG0
    SYSCTL_RCGCGPIO_R |= SYSCTL_RCGCGPIO_R6;                // activate clock for Port N
    while((SYSCTL_PRGPIO_R&SYSCTL_PRGPIO_R6) == 0){};    // allow time for clock to stabilize
    GPIO_PORTG_DIR_R &= 0x00;                                        // make PG0 in (HiZ)
  GPIO_PORTG_AFSEL_R &= ~0x01;                                     // disable alt funct on PG0
  GPIO_PORTG_DEN_R |= 0x01;                                        // enable digital I/O on PG0
                                                                                                    // configure PG0 as GPIO
  //GPIO_PORTN_PCTL_R = (GPIO_PORTN_PCTL_R&0xFFFFFF00)+0x00000000;
  GPIO_PORTG_AMSEL_R &= ~0x01;                                     // disable analog functionality on PN0

    return;
}

//Initialize port J as GPIO with clock
void PortJ_Init(void){
	SYSCTL_RCGCGPIO_R |= SYSCTL_RCGCGPIO_R8;					// activate clock for Port J
	while((SYSCTL_PRGPIO_R&SYSCTL_PRGPIO_R8) == 0){};	// allow time for clock to stabilize
  GPIO_PORTJ_DIR_R &= ~0x02;    										// make PJ1 in 
  GPIO_PORTJ_DEN_R |= 0x02;     										// enable PJ2 digital i/o
	
	GPIO_PORTJ_PCTL_R &= ~0x000000F0;	 								//  PJ1 as GPIO 
	GPIO_PORTJ_AMSEL_R &= ~0x02;											//  disable analog functionality on PJ1		
	GPIO_PORTJ_PUR_R |= 0x02;													//	enable weak pull up resistor
}


//Given Code
//Set XSHUT This pin is an active-low shutdown input; 
//					the board pulls it up to VDD to enable the sensor by default. 
//					Driving this pin low puts the sensor into hardware standby. This input is not level-shifted.
void VL53L1X_XSHUT(void){
    GPIO_PORTG_DIR_R |= 0x01;                                        // make PG0 out
    GPIO_PORTG_DATA_R &= 0b11111110;                                 //PG0 = 0
    FlashAllLEDs();
    SysTick_Wait10ms(10);
    GPIO_PORTG_DIR_R &= ~0x01;                                            // make PG0 input (HiZ)
    
}

//Initialize port H
void PortH_Init(void){
  //Pins of Port M used as output
  SYSCTL_RCGCGPIO_R |= SYSCTL_RCGCGPIO_R7;     // activate clock  
	
  while((SYSCTL_PRGPIO_R&SYSCTL_PRGPIO_R7) == 0){};    // stabilize clock time
  GPIO_PORTH_DIR_R |= 0xFF;                                        // PH0 out
  GPIO_PORTH_AFSEL_R &= ~0xFF;                                     // PH0 disable alt funct 
  GPIO_PORTH_DEN_R |= 0xFF;                                        // PH0 enable digital I/O 
                                                                                                  
  GPIO_PORTH_AMSEL_R &= ~0xFF;                                     // disable analog functionality on PH0        
  return;
}

//Spin function used for motor
void spin(int direction){
		//8 iterations used to get 5.625 degrees
    for(int i=0; i<8; i++){ 
			//Fire up stepper motor coils to make it spin Clockwise
			if(direction == 0) { 
				GPIO_PORTH_DATA_R = 0b00001001;
				SysTick_Wait10ms(1);
				GPIO_PORTH_DATA_R = 0b00000011;
				SysTick_Wait10ms(1);
				GPIO_PORTH_DATA_R = 0b00000110;
				SysTick_Wait10ms(1);
				GPIO_PORTH_DATA_R = 0b00001100;
				SysTick_Wait10ms(1);
			}
			//Fire up stepper motor coils in reverse order to make it spin Counter Clockwise
			else if(direction == 1) { 
				GPIO_PORTH_DATA_R = 0b00001100;
        SysTick_Wait10ms(1);
        GPIO_PORTH_DATA_R = 0b00000110;
        SysTick_Wait10ms(1);
        GPIO_PORTH_DATA_R = 0b00000011;
        SysTick_Wait10ms(1);
        GPIO_PORTH_DATA_R = 0b00001001;
        SysTick_Wait10ms(1);
			}
			else {
				GPIO_PORTH_DATA_R = 0b00000000;
				SysTick_Wait10ms(1);
			}		
    }
		GPIO_PORTH_DATA_R = 0b00000000;
}



//---------------------- Main Function Starts ---------------------- 

//Given
uint16_t	dev = 0x29;			//address of the ToF sensor as an I2C slave peripheral
int status = 0; 

//Main function to control entire program
int main(void) {
	//Inititialize variables needed for TOF sensor
  uint8_t sensorState = 0; 
  uint16_t wordData;
  uint16_t Distance;
  uint8_t dataReady;

	//Intializations
	//Initialize all required systems such as system clock, GPIO ports, I2C, and UART
	PLL_Init();	
	SysTick_Init();
	onboardLEDs_Init();
	PortH_Init();
	PortG_Init();
	PortJ_Init();
	I2C_Init();
	UART_Init();

/* Those basic I2C read functions can be used to check your own I2C functions */
	status = VL53L1X_GetSensorId(dev, &wordData);

	//Have microcontroller boot (turn on) ToF sensor with I2C communication
	while(sensorState==0){
		status = VL53L1X_BootState(dev, &sensorState);
		SysTick_Wait10ms(1);
  }
	
	//Ensure interrupt has been cleared for next one to function
	status = VL53L1X_ClearInterrupt(dev);
	
	//Given
  //Initialize sensor with default settings including distance mode and ranging
  status = VL53L1X_SensorInit(dev);
	//Long mode is used to ensure precise measurements
	status = VL53L1X_SetDistanceMode(dev, 2); 
	status = VL53L1X_StartRanging(dev);
	
	//---- Obtain Measurements ----
	//Run infinitely
  while(1) {
		Restart: 
		//Onboard button previously initialized to be used to check if measurements be taken
		//Check if pressed (active low config)
		if((GPIO_PORTJ_DATA_R&0b00000010) == 0) { 
			//64 measurements to be collected (64*5.625=360) 
			for(int i = 0; i < 64; i++) {
				
				//Wait for ToF sensor
				while (dataReady == 0){
					status = VL53L1X_CheckForDataReady(dev, &dataReady);
					VL53L1_WaitMs(dev, 5);
				}
				
				//I2C communication to obtain distance measurement from ToF sensor
				//LED flash every measurement
				dataReady = 0;
				status = VL53L1X_GetDistance(dev, &Distance);					
				FlashLED4(1);

				//Ensure interrupt has been cleared for next one to function
				status = VL53L1X_ClearInterrupt(dev);
				double dist = Distance;
				//Send distance data to connected PC using UART communication
				sprintf(printf_buffer,"%f\r\n", dist/1000); 
				UART_printf(printf_buffer);
				
				//After every reading, spin in the CCW direction again 5.625 deg
				spin(0); 
				SysTick_Wait10ms(1);
				
				//---- BONUS IMPLEMENTATION ----
				//Check if button is pressed at any moment during measurement calculations (active low config) during measurement collection
				if((GPIO_PORTJ_DATA_R&0b00000010) == 0) {
					//Assigned troubleshooting LED used
					FlashLED2(1);
					//Spin the reverse direction the amount of times already measured and start over
					for(int j = 0; j < i; j++) {
						spin(1);
					}
					goto Restart; 
				}				
				
			}
			//---- Back Home ----
			//Once 64 measurements have been taken, spin in the reverse direction to home position to untangle wires
			for(int i = 0; i < 64; i++) {
				spin(1);
			}
		}
	}
}
