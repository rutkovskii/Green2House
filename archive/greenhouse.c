#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>  //Header file for sleep(). man 3 sleep for details.
#include <pthread.h>
#include <fcntl.h>
#include <string.h>
#include <libconfig.h>  

// A normal C function that is executed as a thread 
// when its name is specified in pthread_create()
void getTemp(float *cTemp, float *fTemp)
{
    int fd; //read from file
    char buf[64];
    snprintf(buf, sizeof(buf), "/sys/bus/iio/devices/iio:device0/in_voltage1_raw", 1);
    char temperature[4];

    fd = open(buf, O_RDONLY);
    read(fd, &temperature, 4);
    close(fd);
    int val = atoi(temperature);
    float voltage = val*1.8/4095;
    *cTemp = (voltage - 0.5)*100;
    *fTemp = *cTemp * 9.0/5.0 + 32.0;
}

void displayData(){
    time_t ltime; /* calendar time */
    ltime=time(NULL); /* get current cal time */
    printf("[%s]",asctime( localtime(&ltime) ) );
}


int main()
{
    float f, c;
    while(1){
        getTemp(&c, &f);
        time_t ltime;
        struct tm result;
        char stime[32];

        ltime = time(NULL);
        localtime_r(&ltime, &result);
        printf("%.2f degrees F at %s\n", c, asctime_r(&result, stime));
        fflush(stdout);
        sleep(60);
    }
    return 0;
}