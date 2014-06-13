__kernel void mandlebrot(__global float* params, 
                                  __global float* c)
{
    float width = params[0];
    float height = params[1];
    float x0 = params[2];
    float y0= params[3];
    float x1 = params[4];
    float y1= params[5];

    unsigned int index = get_global_id(0);

    unsigned int num_iterations = 100;

    unsigned int i = index%(int)width;
    unsigned int j = index/(int)height;
    
    float x = i * (float)(x1-x0)/width + x0;
    float y = j * (float)(y1-y0)/height + y0;

    float zx = 0;
    float zy = 0;
    float xtemp = 0;

    for(int iterations = 0; iterations < num_iterations; iterations ++){
        if(zx*zx + zy*zy > 2*2){
            c[index] = iterations;
            return;
        }

        xtemp = zx*zx - zy*zy + x;
        zy = 2*zx*zy + y;
        zx = xtemp;
    }

    c[index] = num_iterations;
}
