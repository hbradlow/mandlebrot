__kernel void mandlebrot(__global float* width, 
                                  __global float* height, 
                                  __global float* c)
{
    unsigned int index = get_global_id(0);

    unsigned int num_iterations = 100;

    unsigned int i = index%((int)width[0]);
    unsigned int j = index/((int)width[0]);
    
    float x = i*4.f/width[0]-2;
    float y = j*4.f/height[0]-2;

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
