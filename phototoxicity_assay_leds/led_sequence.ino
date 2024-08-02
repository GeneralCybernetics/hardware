/* ----------------------------------------------------------------------
"Pixel dust" Protomatter library example. As written, this is
SPECIFICALLY FOR THE ADAFRUIT MATRIXPORTAL with 64x32 pixel matrix.
Change "HEIGHT" below for 64x64 matrix. Could also be adapted to other
Protomatter-capable boards with an attached LIS3DH accelerometer.

PLEASE SEE THE "simple" EXAMPLE FOR AN INTRODUCTORY SKETCH,
or "doublebuffer" for animation basics.
------------------------------------------------------------------------- */

#include <Wire.h>                 // For I2C communication
#include <Adafruit_LIS3DH.h>      // For accelerometer
#include <Adafruit_PixelDust.h>   // For sand simulation
#include <Adafruit_Protomatter.h> // For RGB matrix

#define HEIGHT  64 // Matrix height (pixels) - SET TO 64 FOR 64x64 MATRIX!
#define WIDTH   64 // Matrix width (pixels)
#define MAX_FPS 45 // Maximum redraw rate, frames/second

#if defined(_VARIANT_MATRIXPORTAL_M4_) // MatrixPortal M4
uint8_t rgbPins[]  = {7, 8, 9, 10, 11, 12};
uint8_t addrPins[] = {17, 18, 19, 20, 21};
uint8_t clockPin   = 14;
uint8_t latchPin   = 15;
uint8_t oePin      = 16;
uint8_t upButton   = 2; 
#else // MatrixPortal ESP32-S3
uint8_t rgbPins[]  = {42, 41, 40, 38, 39, 37};
uint8_t addrPins[] = {45, 36, 48, 35, 21};
uint8_t clockPin   = 2;
uint8_t latchPin   = 47;
uint8_t oePin      = 14;
#endif

#if HEIGHT == 16
#define NUM_ADDR_PINS 3
#elif HEIGHT == 32
#define NUM_ADDR_PINS 4
#elif HEIGHT == 64
#define NUM_ADDR_PINS 5
#endif

Adafruit_Protomatter matrix(
  WIDTH, 4, 1, rgbPins, NUM_ADDR_PINS, addrPins,
  clockPin, latchPin, oePin, true);

Adafruit_LIS3DH accel = Adafruit_LIS3DH();

#define N_COLORS   8
#define BOX_HEIGHT 8
#define N_GRAINS (BOX_HEIGHT*N_COLORS*8)
#define N_L 2
#define N_I 12
uint16_t colors[N_COLORS];
double L[N_L] = {166, 333};
double I[N_I] = {1*60000, 2*60000, 3*60000, 4*60000, 5*60000, 6*60000, 7*60000, 8*60000, 9*60000, 10*60000, 12.5*60000, 15*60000};

int init_well_pos_x;
int init_well_pos_y;

unsigned long prevMillis;

bool alignmentStage = true;

// SETUP - RUNS ONCE AT PROGRAM START --------------------------------------

void err(int x) {
  uint8_t i;
  pinMode(LED_BUILTIN, OUTPUT);       // Using onboard LED
  for(i=1;;i++) {                     // Loop forever...
    digitalWrite(LED_BUILTIN, i & 1); // LED on/off blink to alert user
    delay(x);
  }
}

void setup(void) {
  Serial.begin(115200);
  //while (!Serial) delay(10);

  ProtomatterStatus status = matrix.begin();
  Serial.printf("Protomatter begin() status: %d\n", status);

  colors[0] = matrix.color565(64, 64, 64);  // Dark Gray
  colors[1] = matrix.color565(120, 79, 23); // Brown
  colors[2] = matrix.color565(228,  3,  3); // Red
  colors[3] = matrix.color565(255,140,  0); // Orange
  colors[4] = matrix.color565(255,237,  0); // Yellow
  colors[5] = matrix.color565(  0,128, 38); // Green
  colors[6] = matrix.color565(  0, 77,255); // Blue
  colors[7] = matrix.color565(117,  7,135); // Purple

  // well_pos_x = {5, 17};
  init_well_pos_x = 5;
  init_well_pos_y = matrix.height()-15;

  pinMode(upButton, INPUT_PULLUP);

}

// MAIN LOOP - RUNS ONCE PER FRAME OF ANIMATION ----------------------------

void loop() {

  // Update pixel data in LED driver
  // dimension_t x, y;
  matrix.fillScreen(0x0);

  if (digitalRead(upButton) == false) {
    matrix.drawPixel(0, 0, colors[0]);
    matrix.drawPixel(63, 0, colors[1]);
    matrix.drawPixel(0, 63, colors[2]);
    matrix.drawPixel(63, 63, colors[3]);
    alignmentStage = false;
  }

  // ----------------- alignment stage ------------------------
  if (alignmentStage) {
    // make the red outline 
    for (int x=0; x<(int)matrix.width()/2; x++) {
      matrix.drawPixel(9, x, colors[2]);
    }
    for (int x=0; x<(int)matrix.width()/2; x++) {
      matrix.drawPixel(10, x, colors[2]);
    }
    for (int y=11; y<matrix.height()-10; y++) {
      matrix.drawPixel(y, 0, colors[2]);
      matrix.drawPixel(y, 1, colors[2]);
      matrix.drawPixel(y, (int)matrix.width()/2-1, colors[2]);
    }
    for (int y=matrix.height()-10; y<matrix.height()-6; y++) {
      for(int x=y-(matrix.height()-10); x<(int)matrix.width()/2-(y-(matrix.height()-10)); x++) {
        // Serial.println((int)y, (int)x);
        matrix.drawPixel(y, x, colors[2]);
      }
    }

    // illuminate wells
    uint16_t blue = matrix.color565(0, 0, 255); // White color
    for (int i = 0; i < (sizeof(L)/sizeof(L[0]))*4; i++) {
      for (int j = 0; j < sizeof(I)/sizeof(I[0]); j++) {
        int x = init_well_pos_x + i * 3; // 4 pixels per well
        int y = init_well_pos_y -  j * 3;
        for (int dx = 0; dx < 2; dx++) {
          for (int dy = 0; dy < 2; dy++) {
            matrix.drawPixel(y + dy, x + dx, blue);
          }
        }
      }
    }

  }

  
  

  matrix.show(); // Copy data to matrix buffers
}